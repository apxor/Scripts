db = db.getSiblingDB("admin");
dbs = db.runCommand({ "listDatabases": 1 }).databases;

dbs.forEach(function(database) {
    db = db.getSiblingDB(database.name);
    cols = db.getCollectionNames();

    cols.forEach(function(col) {
    	if(col === "something"){
    		db.getCollection(col).updateMany({}, {$set: {/*Something*/}})
    		print(database.name)
        	print(col);
    	}
    });
});
