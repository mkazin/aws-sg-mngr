
CREATE TABLE registeredCidrs (
    id integer PRIMARY KEY AUTOINCREMENT,
    cidr text NOT NULL, 
    description text NULL,
    location text NULL,
    owner text NULL,
    expiration integer NULL
)