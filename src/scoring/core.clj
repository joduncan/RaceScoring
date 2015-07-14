(ns scoring.core
    (:require [clojure.string :as string])
    (:require [clj-time.core :as t :only [date-time]])
    ;(:require [clj-time.format :as f])
    (:require [clojure.data.csv :as csv]
	      [clojure.java.io  :as io]))


(defn l[] (use 'scoring.core :reload))

(defn int-or-nil[data]
  (try (Integer. data) (catch Exception e nil)))

(defn parse-time-or-nil[ time ] time
  (try
   (let [[intpart dec](string/split time #"\.")
	[ss mm hh](reverse (map #(Integer. %) (string/split intpart #":")))
	[hours minutes seconds](map #(if (nil? %) 0 %) [hh mm ss])]
	(+ (* 60 60 hours) (* 60 minutes) seconds (Float. (string/join "" ["0." dec]))))
   (catch Exception e nil))
  )
  
(defn to-sex[data]
  (case (first (string/upper-case data))
    \F :female
    \M :male
    nil))

(defn list-getter[lst]
  #(try (nth lst %) (catch Exception e "")))

; TODO: flip it when the format is last, first 
(defn row-to-athlete-result[race-id row]
  (let [itm (comp string/trim (list-getter row))]
    {:name (itm 1)
     :age  (int-or-nil (itm 2))
     :sex  (to-sex (itm 3))
     :time (parse-time-or-nil (itm 4))
     :race-id race-id} ))

(defn scores[base]
  "an infinite list of descending scores per rank starting with the base score"
  (map (fn[i]{:score (* base (/ 5 (+ 5 i)))}) (range)))
(def scores (memoize scores))

(defn ranking-list
  "an infinite list of ranks, used for females, males, and overall" 
  [key] (map (fn[i]{key (+ i 1)}) (range))) 
(def ranking-list (memoize ranking-list))

(defn to-race-struct[filename data race-id]
  ;(prn "loading" filename)
  (let [itm        (fn[i](string/trim (get (nth data i) 0)))
        points     (Integer. (itm 3))
	racers     (map merge (map (partial row-to-athlete-result race-id) (drop 4 data)) (ranking-list :overall-rank))
	score-list (scores points)
	sexer      (fn[sex rank-key] (map merge (filter (fn[athlete](= (:sex athlete) sex)) racers) score-list (ranking-list rank-key)))
 ]
  {:name          (itm 0)
   :date          (apply t/date-time (map #(Integer. %) (string/split (itm 1) #"-")))
   :url           (itm 2)
   :points        points
   :male-racers   (sexer :male :male-rank)
   :female-racers (sexer :female :female-rank)
   :race-id race-id
   }))
  
(defn load-race-data[fn id]  
  (with-open [in-file (io/reader fn)]
     	     (to-race-struct fn (doall (csv/read-csv in-file)) id)))

(defn load-all-races[]
  (map load-race-data (rest (file-seq (java.io.File. "data")))(range)))

(def races (load-all-races))

(def race-map (apply hash-map (apply concat (map (fn[race][(:race-id race) race]) races))))

(defn flatten-racers[gender] (apply concat (map gender races)))


(defn athlete-comparator[a1 a2] 
  (let [name-comparison (compare (:name a1) (:name a2))
        null-to-zero #(if (nil? %) 0 %)
	age-1 (null-to-zero (:age a1))
	age-2 (null-to-zero (:age a2))]
	(if (zero? name-comparison)
	    (- age-2 age-1)
	    name-comparison)))
	
(def male-athletes (sort athlete-comparator (flatten-racers :male-racers)))


(defn make-scores[ args ]
  (print "making scores"))

