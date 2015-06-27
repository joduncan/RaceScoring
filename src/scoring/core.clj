(ns scoring.core
    ;(:use [clojure.string])
    (:require [clojure.data.csv :as csv]
	      [clojure.java.io  :as io]))

(use 'clojure.string)

(defn l[] (use 'scoring.core :reload))

(defn to-race-struct[fn data]
  (println "loading" fn)
  (let [itm #(trim (get (nth data %) 0))] 
  {:name   (itm 0)
   :date   (itm 1)
   :url    (itm 2)
   :points (Integer. (itm 3))
   }))
  
(defn load-race-data[fn]  
  (with-open [in-file (io/reader fn)]
     	     (to-race-struct fn (doall (csv/read-csv in-file)))))

(defn load-all-races[]
  (map load-race-data (rest (file-seq (java.io.File. "data")))))

(defn make-scores[ args ]
  (print "making scores"))

