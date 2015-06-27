(defproject cartman "0.0.1"
  :description "USASCA scoring system"
  :dependencies [[org.clojure/clojure "1.6.0"]
                 [org.clojure/data.csv "0.1.2"]
                 [clj-time "0.7.0"]
                 [org.clojure/core.memoize "0.5.6"]
                 ]

  :aot [scoring.core]
  :main scoring.core

  ;:plugins [[lein-ring "0.8.8"]]

  ;:ring {:handler scoring.core/app
   ;      :init    scoring.core/scoring-start}
   )
