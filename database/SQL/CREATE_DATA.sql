-- Fill out the data tables.
INSERT INTO "User" (UserName) VALUES ('{self.__user_name}');
INSERT INTO "Alerts" (AlertsType, StandardSound, OwnSound) VALUES ('Off', '\Sound\StandardSound.mp3', (NULL));
INSERT INTO "Autorun" (EnableProgram, EnableMic, MicStatus, WalkieStatus) VALUES (1, 1, 1, 0);
INSERT INTO "Hotkey" (HotkeyMic, HotkeyWalkie) VALUES ('Scroll lock', 'HOME');
INSERT INTO "Settings" (LanguageCode, NightTheme, PrivacyStatus) VALUES ('rus', 1, 0);
INSERT INTO "About" SET (ProgramVersion, WebSite, Email, Copyright, UrlPrivacyPolicy) VALUES ('v.1.2022.02.14', 'https://controlmictray.pp.ua/', 'info@controlmictray.pp.ua', 'Copyright © 2022\nSimonovskiy & Lastivka\nAll rights reserved', 'https://controlmictray.pp.ua/PrivacyPolicy.html');