CREATE TABLE "User" (                             -- Create a table.
	"ID"                NOT NULL UNIQUE,          -- Create a numeric field, be sure to fill, unique value.
	"UserName"          VARCHAR(254) NOT NULL,    -- Create a text field, be sure to fill.
	PRIMARY KEY("ID" AUTOINCREMENT)               -- We indicate where the keys 🔑 and the fields with the meter.
);
CREATE TABLE "Alerts" (                           -- Create a table.
	"ID"                INTEGER NOT NULL UNIQUE,  -- Create a numeric field, be sure to fill, unique value.
	"AlertsType"        VARCHAR(254) NOT NULL,    -- Create a text field, be sure to fill.
	"StandardSound"     VARCHAR(254) NOT NULL,    -- Create a text field, be sure to fill.
	"OwnSound"          VARCHAR(254),             -- Create a text field.
	FOREIGN KEY("ID")   REFERENCES "User"("ID"),  -- We specify which field is related to the field from another table.
	PRIMARY KEY("ID" AUTOINCREMENT)               -- We indicate where the keys 🔑 and the fields with the meter.
);
CREATE TABLE "Autorun" (                          -- Create a table.
	"ID"                INTEGER NOT NULL UNIQUE,  -- Create a numeric field, be sure to fill, unique value.
	"EnableProgram"     INTEGER NOT NULL,         -- Create a numeric field, be sure to fill.
	"EnableMic"         INTEGER NOT NULL,         -- Create a numeric field, be sure to fill.
	"MicStatus"         INTEGER NOT NULL,         -- Create a numeric field, be sure to fill.
	"WalkieStatus"      INTEGER NOT NULL,         -- Create a numeric field, be sure to fill.
	FOREIGN KEY("ID")   REFERENCES "User"("ID"),  -- We specify which field is related to the field from another table.
	PRIMARY KEY("ID" AUTOINCREMENT)               -- We indicate where the keys 🔑 and the fields with the meter.
);
CREATE TABLE "Hotkey" (                           -- Create a table.
	"ID"                INTEGER NOT NULL UNIQUE,  -- Create a numeric field, be sure to fill, unique value.
	"HotkeyMic"         VARCHAR(32),              -- Create a text field.
	"HotkeyWalkie"      VARCHAR(32),              -- Create a text field.
	FOREIGN KEY("ID")   REFERENCES "User"("ID"),  -- We specify which field is related to the field from another table.
	PRIMARY KEY("ID" AUTOINCREMENT)               -- We indicate where the keys 🔑 and the fields with the meter.
);
CREATE TABLE "Settings" (                         -- Create a table.
	"ID"                INTEGER NOT NULL UNIQUE,  -- Create a numeric field, be sure to fill, unique value.
	"LanguageCode"      VARCHAR(4) NOT NULL,      -- Create a text field, be sure to fill.
	"NightTheme"        INTEGER NOT NULL,         -- Create a numeric field, be sure to fill.
	"PrivacyStatus"     INTEGER NOT NULL,         -- Create a numeric field, be sure to fill.
	FOREIGN KEY("ID")   REFERENCES "User"("ID"),  -- We specify which field is related to the field from another table.
	PRIMARY KEY("ID" AUTOINCREMENT)               -- We indicate where the keys 🔑 and the fields with the meter.
);
CREATE TABLE "About" (                            -- Create a table.
	"ID"                INTEGER NOT NULL UNIQUE,  -- Create a numeric field, be sure to fill, unique value.
	"ProgramVersion"    VARCHAR(32) NOT NULL,     -- Create a text field, be sure to fill.
	"WebSite"           VARCHAR(32) NOT NULL,     -- Create a text field, be sure to fill.
	"Email"             VARCHAR(32) NOT NULL,     -- Create a text field, be sure to fill.
	"Copyright"         VARCHAR(64) NOT NULL,     -- Create a text field, be sure to fill.
	"UrlPrivacyPolicy"  VARCHAR(64) NOT NULL,     -- Create a text field, be sure to fill.
	PRIMARY KEY("ID" AUTOINCREMENT)               -- We indicate where the keys 🔑 and the fields with the meter.
);