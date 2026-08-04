#!/usr/bin/env ruby

require "json"


def fail!(id, message, code)
  warn "#{id}: #{message}"
  exit code
end


def compile_source(source, id)
  eval(source, TOPLEVEL_BINDING, id)
  method(:benchmark)
rescue StandardError, SyntaxError => error
  fail!(id, "could not compile source: #{error.message}", 1)
end


mode, id, source_hex, expected, windows_text, calls_text, *extra = ARGV
if !extra.empty? ||
   [mode, id, source_hex, expected, windows_text, calls_text].any?(&:nil?)
  fail!("ruby_runner", "expects MODE ID SOURCE_HEX EXPECTED WINDOWS CALLS", 2)
end
unless ["prepared", "eval"].include?(mode)
  fail!(id, "unsupported mode #{mode}", 2)
end
unless defined?(RubyVM::YJIT) && RubyVM::YJIT.enabled?
  fail!(id, "YJIT is not enabled; run Ruby with --yjit", 2)
end

source = [source_hex].pack("H*")
windows = Integer(windows_text, 10)
calls = Integer(calls_text, 10)
if windows.negative? || calls < 1
  fail!(id, "WINDOWS must be non-negative and CALLS must be positive", 2)
end

prepared = nil
prepare_ns = nil
if mode == "prepared"
  started = Process.clock_gettime(Process::CLOCK_MONOTONIC, :nanosecond)
  prepared = compile_source(source, id)
  prepare_ns =
    Process.clock_gettime(Process::CLOCK_MONOTONIC, :nanosecond) - started
end

evaluate = lambda do
  callable = prepared || compile_source(source, id)
  value = callable.call
  fail!(id, "expected #{expected}, got #{value}", 1) unless value.to_s == expected
end

started = Process.clock_gettime(Process::CLOCK_MONOTONIC, :nanosecond)
evaluate.call
first_ns =
  Process.clock_gettime(Process::CLOCK_MONOTONIC, :nanosecond) - started
samples = Array.new(windows) do
  started = Process.clock_gettime(Process::CLOCK_MONOTONIC, :nanosecond)
  calls.times { evaluate.call }
  (Process.clock_gettime(Process::CLOCK_MONOTONIC, :nanosecond) - started) / calls
end

stats = RubyVM::YJIT.respond_to?(:runtime_stats) ? RubyVM::YJIT.runtime_stats : {}
puts JSON.generate(
  runtime: "ruby-yjit",
  workload: id,
  prepare_ns: prepare_ns,
  first_ns: first_ns,
  samples_ns: samples,
  yjit_enabled: true,
  yjit_compiled_iseq_count: stats[:compiled_iseq_count]
)
