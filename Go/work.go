package main

import (
	"database/sql"
	"flag"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"lang"
	"log"
	"os"
	"os/exec"
	"text/tabwriter"
	"time"
)

var tabw *tabwriter.Writer
var DEBUG *bool
var NODE *string
var SUBJECT *string

func init() {
	//log flags
	log.SetFlags(log.LstdFlags | log.Lshortfile)
	//tabwriter Init
	tabw = new(tabwriter.Writer)
	tabw.Init(os.Stdout, 0, 8, 0, '\t', 0)
	//command line flags
	DEBUG = flag.Bool("debug", false, "Debug Mode")
	NODE = flag.String("n", "", "node name, can be just cluster name for all of that cluster")
	SUBJECT = flag.String("subject", "", "subject matter, searches kickstand events for this string")
	flag.Parse()

}

type issue struct {
	hostname    string
	pbs_comment string
	subject     string
}

func dbConnect() *sql.DB {
	addr := "memoriae.rcac.purdue.edu:3306"
	user := "cmdbuser"
	pass := "9N6ncyraekjD"
	dbname := "rcac_cmdb"

	db, err := sql.Open("mysql", user+":"+pass+"@("+addr+")/"+dbname)
	if err != nil {
		log.Fatal(err)
	}
	err = nil
	err = db.Ping()
	if err != nil {
		log.Fatal(err)
	}

	return db
}

func dbQueryInit() string {
	columns := "hostnameshort, pbs_comment, subject"
	tables := "hosts, events"
	condition := "hostnameshort LIKE '%" + *NODE + "%' AND hosts.id = events.hostid AND status = 'open'"
	condition += " AND subject LIKE '%" + *SUBJECT + "%' AND active = 'Y'"
	exclude := "AND pbs_comment NOT LIKE '%: %'"

	query := "SELECT " + columns
	if tables != "" {
		query += " FROM " + tables
	}
	if condition != "" {
		query += " WHERE " + condition
	}
	if exclude != "" {
		query += exclude
	}

	query += " GROUP BY hostnameshort"

	println(query + "\n")
	return query

}

func dbQueryRun(db *sql.DB) (rows *sql.Rows) {
	db.Ping()
	query := dbQueryInit()
	//Run db Query
	rows, err := db.Query(query)
	if err != nil {
		log.Fatal(err)
	}

	if err := rows.Err(); err != nil {
		log.Fatal(err)
	}

	return rows
}

//returns 0 or 1
// 0 = NOT pingable
// 1 = pingable
func nodeConnect(node string) (int, err) {
	fmt.Println(node)
	cmd := exec.Command("ping", "-c 5", node)
	//cmd.Stdout = os.Stdout
	//cmd.Stderr = os.Stderr
	//cmd.Stdin = os.Stdin

	cmd.Start()
	donec := make(chan error, 1)
	go func() {
		donec <- cmd.Wait()
	}()
	select {
	case <-time.After(5 * time.Second):
		cmd.Process.Kill()
		fmt.Println("timeout")
		return 0
	case <-donec:
		fmt.Println("done")
	}

	return 1

}

func main() {
	db := dbConnect()
	rows := dbQueryRun(db)
	for rows.Next() {
		var hostname, pbs_comment, sub string
		rows.Scan(&hostname, &pbs_comment, &sub)
		nodeConnect(hostname)
	}
	fmt.Println("ping complete\n")
}
