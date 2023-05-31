CREATE TABLE "Movimientos" (
	"id"	INTEGER,
	"Fecha"	TEXT,
	"Hora"	TEXT,
	"Moneda_from"	INTEGER NOT NULL,
	"Cantidad_from"	REAL NOT NULL,
	"Moneda_to"	INTEGER NOT NULL,
	"Cantidad_to"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
)