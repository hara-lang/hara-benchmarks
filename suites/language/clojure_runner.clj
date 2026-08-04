#!/usr/bin/env clojure

(ns hara-bench.clojure-runner
  (:require [clojure.string :as str]))

(defn fail!
  [id message code]
  (binding [*out* *err*]
    (println (str id ": " message)))
  (System/exit code))

(defn hex-decode
  [value]
  (apply str
         (map #(char (Integer/parseInt % 16))
              (re-seq #".." value))))

(defn -main
  [& arguments]
  (let [[mode id source-hex expected windows-text calls-text & extra] arguments]
    (when (or (seq extra)
              (some nil? [mode id source-hex expected windows-text calls-text]))
      (fail! "clojure_runner"
             "expects MODE ID SOURCE_HEX EXPECTED WINDOWS CALLS"
             2))
    (when-not (or (= mode "prepared") (= mode "eval"))
      (fail! id (str "unsupported mode " mode) 2))
    (let [windows (parse-long windows-text)
          calls (parse-long calls-text)
          source (hex-decode source-hex)
          prepare-started (System/nanoTime)
          prepared (when (= mode "prepared")
                     (eval (read-string (str "(fn [] " source ")"))))
          prepare-ns (when prepared
                       (- (System/nanoTime) prepare-started))
          evaluate (fn []
                     (let [value (if prepared
                                   (prepared)
                                   (eval (read-string source)))]
                       (when-not (= (str value) expected)
                         (fail! id
                                (str "expected " expected ", got " value)
                                1))))
          started (System/nanoTime)]
      (evaluate)
      (let [first-ns (- (System/nanoTime) started)
            samples (mapv (fn [_]
                            (let [window-started (System/nanoTime)]
                              (dotimes [_ calls]
                                (evaluate))
                              (quot (- (System/nanoTime) window-started)
                                    calls)))
                          (range windows))]
        (println
          (str "{\"runtime\":\"clojure\",\"workload\":\"" id
               "\",\"prepare_ns\":" (or prepare-ns "null")
               ",\"first_ns\":" first-ns
               ",\"samples_ns\":[" (str/join "," samples) "]}"))))))

(apply -main *command-line-args*)
(shutdown-agents)
