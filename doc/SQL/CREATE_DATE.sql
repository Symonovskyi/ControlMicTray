-- Заполняем таблицы данными.
INSERT INTO "User" (UserName) VALUES ('{self.__user_name}');
INSERT INTO "Alerts" (AlertsType, StandardSound, OwnSound) VALUES ('Off', '\Sound\StandardSound.mp3', (NULL));
INSERT INTO "Autorun" (EnableProgram, EnableMic) VALUES (1, 1);
INSERT INTO "Hotkey" (HotkeyMic, HotkeyWalkie) VALUES ('Scroll lock', 'HOME');
INSERT INTO "Settings" (LanguageCode, NightTheme, PrivacyStatus) VALUES ('rus', 1, 0);
INSERT INTO "About" (ProgramVersion, WebSite, Email, Copyright, UrlPrivacyPolicy) VALUES ('v.1.2022.01.31-alpha', 'https://controlmictray.pp.ua/', 'info@controlmictray.pp.ua', 'Copyright © 2022\nSimonovskiy & Lastivka\nAll rights reserved', 'https://controlmictray.pp.ua/PrivacyPolicy.html');