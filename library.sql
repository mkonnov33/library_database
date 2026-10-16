CREATE TABLE IF NOT EXISTS "accounts" (
	"id" INTEGER NOT NULL,
	"username" TEXT NOT NULL,
	"password" TEXT NOT NULL,
	"employee" BOOLEAN,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "reservations"("account_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id") REFERENCES "employees"("account_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "books" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"release_date" TEXT NOT NULL,
	"author_id" INTEGER NOT NULL,
	"genre_id" INTEGER,
	"featured_in_event" BOOLEAN,
	"event_id" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "reservations"("book_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "authors" (
	"id" INTEGER NOT NULL,
	"first_name" TEXT NOT NULL,
	"last_name" TEXT NOT NULL,
	"date_of_birth" DATE,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "books"("author_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "reservations" (
	"id" INTEGER NOT NULL,
	"book_id" INTEGER NOT NULL,
	"account_id" INTEGER NOT NULL,
	"library_id" INTEGER NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "libraries" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"address" TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "reservations"("library_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id") REFERENCES "events"("library_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id") REFERENCES "employees"("library_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "events" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"library_id" INTEGER NOT NULL,
	"starting_date" INTEGER NOT NULL,
	"ending_date" INTEGER NOT NULL,
	"active" BOOLEAN NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "books"("event_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "employees" (
	"id" INTEGER NOT NULL,
	"first_name" TEXT NOT NULL,
	"last_name" TEXT NOT NULL,
	"age" INTEGER,
	"library_id" INTEGER NOT NULL,
	"account_id" INTEGER NOT NULL,
	"position_id" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "leaves"("employee_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "leaves" (
	"id" INTEGER NOT NULL,
	"employee_id" INTEGER NOT NULL,
	"paid" BOOLEAN NOT NULL,
	"cause" TEXT NOT NULL,
	"start_date" DATE NOT NULL,
	"end_date" DATE NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "positions" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"available" BOOLEAN NOT NULL,
	"salary" REAL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "employees"("position_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "genres" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"description" TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "books"("genre_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
