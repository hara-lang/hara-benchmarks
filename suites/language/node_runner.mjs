#!/usr/bin/env node

import process from 'node:process';

function fail(id, message, code) {
  console.error(`${id}: ${message}`);
  process.exit(code);
}

function decodeHex(value) {
  return Buffer.from(value, 'hex').toString('utf8');
}

function compile(source, id) {
  try {
    return new Function(`"use strict";\n${source}\nreturn benchmark;`)();
  } catch (error) {
    fail(id, `could not compile source: ${error.message}`, 1);
  }
}

const [mode, id, sourceHex, expected, windowsText, callsText, ...extra] =
  process.argv.slice(2);

if (
  extra.length ||
  [mode, id, sourceHex, expected, windowsText, callsText].some(
    value => value === undefined,
  )
) {
  fail('node_runner', 'expects MODE ID SOURCE_HEX EXPECTED WINDOWS CALLS', 2);
}
if (mode !== 'prepared' && mode !== 'eval') {
  fail(id, `unsupported mode ${mode}`, 2);
}

const windows = Number.parseInt(windowsText, 10);
const calls = Number.parseInt(callsText, 10);
if (
  !Number.isSafeInteger(windows) ||
  windows < 0 ||
  !Number.isSafeInteger(calls) ||
  calls < 1
) {
  fail(id, 'WINDOWS must be non-negative and CALLS must be positive', 2);
}

const source = decodeHex(sourceHex);
let prepared = null;
let prepareNs = null;
if (mode === 'prepared') {
  const started = process.hrtime.bigint();
  prepared = compile(source, id);
  prepareNs = Number(process.hrtime.bigint() - started);
}

function evaluate() {
  const benchmark = prepared ?? compile(source, id);
  const value = benchmark();
  if (String(value) !== expected) {
    fail(id, `expected ${expected}, got ${value}`, 1);
  }
}

let started = process.hrtime.bigint();
evaluate();
const firstNs = Number(process.hrtime.bigint() - started);
const samples = [];
for (let window = 0; window < windows; window++) {
  started = process.hrtime.bigint();
  for (let call = 0; call < calls; call++) evaluate();
  samples.push(Number(process.hrtime.bigint() - started) / calls);
}

console.log(
  JSON.stringify({
    runtime: 'node',
    workload: id,
    prepare_ns: prepareNs,
    first_ns: firstNs,
    samples_ns: samples,
  }),
);
