-- Fill out the data tables.
INSERT INTO "Alerts" (AlertsType, StandardSound, OwnSound) VALUES ('Off', '\Sound\StandardSound.mp3', (NULL));
INSERT INTO "Autorun" (EnableProgram, EnableMic, MicStatus, WalkieStatus) VALUES (1, 0, 1, 0);
INSERT INTO "Hotkey" (HotkeyMic, HotkeyWalkie) VALUES ('Scroll_lock', 'Pause');
INSERT INTO "Settings" (LanguageCode, NightTheme, PrivacyStatus) VALUES ('ru', 1, 0);
INSERT INTO "About" (ProgramVersion, WebSite, Email, Copyright, UrlPrivacyPolicy) VALUES ('v.2022.10.05', 'controlmictray.pp.ua', 'i@controlmictray.pp.ua', 'Copyright © 2022\nSimonovskiy & Lastivka\nAll rights reserved', 'https://controlmictray.pp.ua/PrivacyPolicy.html');