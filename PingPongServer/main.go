package main

import ("encoding/json"; "log"; "net/http")

func main() {
	http.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"response": "pong"})
	})
	log.Println("Server starting on http://localhost:8081")
	log.Fatal(http.ListenAndServe(":8081", nil))
}
