-- *********************************************
-- * SQL MySQL generation                      
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Thu Apr 27 12:45:23 2023 
-- * LUN file: C:\Users\esteb\OneDrive\Bureau\Unif\2 ème année\Q2\BD 2\Projet-BD\Schémas\Camping-era.lun 
-- * Schema: camping_physique/1-1 
-- ********************************************* 


-- Database Section
-- ________________ 

-- create database camping_physique;
use camping_physique;


-- Tables Section
-- _____________ 

create table ACTIVITE (
     Id_acti int not null AUTO_INCREMENT,
     Date_acti date not null,
     Heure varchar(250) not null,
     Lieu varchar(250) not null,
     Id_type_acti int not null,
     Id_anim int,
     constraint ID_ACTIVITE_ID primary key (Id_acti));

create table ADMINISTRATION (
     Id_admin int not null AUTO_INCREMENT,
     Id_staff int,
     constraint ID_ADMINISTRATION_ID primary key (Id_admin),
     constraint FKSTA_ADM_ID unique (Id_staff));

create table ANIMATEUR (
     Id_anim int not null AUTO_INCREMENT,
     Id_staff int,
     constraint ID_ANIMATEUR_ID primary key (Id_anim),
     constraint FKSTA_ANI_ID unique (Id_staff));

create table CLIENT (
     Id_cli int not null AUTO_INCREMENT,
     Id_Pers int not null,
     Pays varchar(250),
     Code_postal int,
     Ville varchar(250),
     Numero_de_maison int,
     Con_Email varchar(250),
     Con_Telephone int,
     Id_equipe int,
     constraint ID_CLIENT_ID primary key (Id_cli),
     constraint FKPER_CLI_ID unique (Id_Pers));

create table cuisine (
     Id_cuisine int not null AUTO_INCREMENT,
     Id_cuis int,
     Id_emplacement int,
     Id_tournoi int,
     constraint ID_cuisine_ID primary key (Id_cuisine));

create table CUISINIER (
     Id_cuis int not null AUTO_INCREMENT,
     Id_staff int,
     constraint ID_CUISINIER_ID primary key (Id_cuis),
     constraint FKSTA_CUI_ID unique (Id_staff));

create table EMPLACEMENT (
     Id_emplacement int not null AUTO_INCREMENT,
     Type_emplacement varchar(250) not null,
     Occupation boolean not null,
     Prix float(1) not null,
     bbq boolean not null,
     nbr_places int not null,
     acces_eau boolean not null,
     Cuisinier boolean not null,
     constraint ID_EMPLACEMENT_ID primary key (Id_emplacement));

create table EQUIPE (
     Id_equipe int not null AUTO_INCREMENT,
     Nom varchar(250) not null,
     Nbr_pers int not null,
     Nbr_PersMax int not null,
     constraint ID_EQUIPE_ID primary key (Id_equipe));

create table FICHE_COMPTA (
     Id_fiche_compta int not null AUTO_INCREMENT,
     Date_fiche date not null,
     Prix_total float(1) not null,
     Id_admin int,   
     constraint ID_FICHE_COMPTA_ID primary key (Id_fiche_compta));

create table inscription (
     Id_acti int not null,
     Id_cli int not null,
     constraint ID_inscription_ID primary key (Id_acti, Id_cli));

create table loue_emplacement (
     Id_cli int not null,
     Id_emplacement int not null,
     Date_debut date not null,
     Date_fin date not null,
     constraint ID_loue_emplacement_ID primary key (Id_emplacement, Id_cli));

create table Loue_mat (
     Id_cli int not null,
     Id_mat int not null,
     Date_loc date not null,
     constraint ID_Loue_mat_ID primary key (Id_mat, Id_cli));

create table MATERIEL (
     Id_mat int not null AUTO_INCREMENT,
     Nom varchar(250) not null,
     Type_mat varchar(250) not null,
     Prix int not null,
     Etat varchar(250) not null,
     Id_admin int,
     constraint ID_MATERIEL_ID primary key (Id_mat));

create table NETTOIE (
     Id_tech int,
     Date_net date not null,
     Heure varchar(250) not null,
     Id_secteur int not null,
     constraint ID_NETTOIE_ID primary key (Heure, Date_net));

create table participe (
     Id_equipe int not null,
     Id_tournoi int not null,
     constraint ID_participe_ID primary key (Id_tournoi, Id_equipe));

create table PERSONNE (
     Nom varchar(250),
     Age int not null,
     Id_Pers int not null AUTO_INCREMENT,
     Mot_de_passe varchar(250) not null,
     STAFF int,
     CLIENT int,
     constraint ID_PERSONNE_ID primary key (Id_Pers));

create table peut_faire (
     Id_anim int not null,
     Id_type_acti int not null,
     constraint ID_peut_faire_ID primary key (Id_type_acti, Id_anim));

create table Prenom (
     Id_Pers int not null,
     Prenom varchar(250) not null);

create table SECTEUR (
     Id_secteur int not null AUTO_INCREMENT,
     Nom varchar(250) not null,
     constraint ID_SECTEUR_ID primary key (Id_secteur));

create table STAFF (
     Id_staff int not null AUTO_INCREMENT,
     Id_Pers int not null,
     Prix float(1) not null,
     Prix_chef float(1),
     TECHNICIEN int,
     CUISINIER int,
     ANIMATEUR int,
     ADMINISTRATION int,
     Employe_ int,
     constraint ID_STAFF_ID primary key (Id_staff),
     constraint FKPER_STA_ID unique (Id_Pers));

create table TECHNICIEN (
     Id_tech int not null AUTO_INCREMENT,
     Id_staff int,
     constraint ID_TECHNICIEN_ID primary key (Id_tech),
     constraint FKSTA_TEC_ID unique (Id_staff));

create table TOURNOI (
     Id_tournoi int not null AUTO_INCREMENT,
     Id_acti int not null,
     Date_tournoi date not null,
     Heure varchar(250) not null,
     Lieu varchar(250) not null,
     Prix float(1) not null,
     constraint ID_TOURNOI_ID primary key (Id_tournoi),
     constraint FKde_ID unique (Id_acti));

create table TYPE_ACTI (
     Id_type_acti int not null AUTO_INCREMENT,
     Prix float(1) not null,
     Taille_min_ int not null comment 'en cm',
     Age_min int not null,
     Nom varchar(250) not null,
     constraint ID_TYPE_ACTI_ID primary key (Id_type_acti));


-- Constraints Section
-- ___________________ 

alter table ACTIVITE add constraint FKde__FK
     foreign key (Id_type_acti)
     references TYPE_ACTI (Id_type_acti);

alter table ACTIVITE add constraint FKanime_FK
     foreign key (Id_anim)
     references ANIMATEUR (Id_anim);

alter table ADMINISTRATION add constraint FKSTA_ADM_FK
     foreign key (Id_staff)
     references STAFF (Id_staff);

-- Not implemented
-- alter table ANIMATEUR add constraint ID_ANIMATEUR_CHK
--     check(exists(select * from peut_faire
--                  where peut_faire.Id_anim = Id_anim)); 

alter table ANIMATEUR add constraint FKSTA_ANI_FK
     foreign key (Id_staff)
     references STAFF (Id_staff);

-- Not implemented
-- alter table CLIENT add constraint ID_CLIENT_CHK
--     check(exists(select * from loue_emplacement
--                  where loue_emplacement.Id_cli = Id_cli)); 

alter table CLIENT add constraint FKPER_CLI_FK
     foreign key (Id_Pers)
     references PERSONNE (Id_Pers);

alter table CLIENT add constraint FKfait_partie_FK
     foreign key (Id_equipe)
     references EQUIPE (Id_equipe);

alter table cuisine add constraint FKcui_TOU_FK
     foreign key (Id_tournoi)
     references TOURNOI (Id_tournoi);

alter table cuisine add constraint FKcui_EMP
     foreign key (Id_emplacement)
     references EMPLACEMENT (Id_emplacement);

alter table cuisine add constraint FKcui_CUI_FK
     foreign key (Id_cuis)
     references CUISINIER (Id_cuis);

alter table CUISINIER add constraint FKSTA_CUI_FK
     foreign key (Id_staff)
     references STAFF (Id_staff);

-- Not implemented
-- alter table EQUIPE add constraint ID_EQUIPE_CHK
--     check(exists(select * from CLIENT
--                  where CLIENT.Id_equipe = Id_equipe)); 

alter table FICHE_COMPTA add constraint FKgere2_FK
     foreign key (Id_admin)
     references ADMINISTRATION (Id_admin);

alter table inscription add constraint FKins_CLI_FK
     foreign key (Id_cli)
     references CLIENT (Id_cli);

alter table inscription add constraint FKins_ACT
     foreign key (Id_acti)
     references ACTIVITE (Id_acti);

alter table loue_emplacement add constraint FKlou_EMP
     foreign key (Id_emplacement)
     references EMPLACEMENT (Id_emplacement);

alter table loue_emplacement add constraint FKlou_CLI_1_FK
     foreign key (Id_cli)
     references CLIENT (Id_cli);

alter table Loue_mat add constraint FKLou_MAT
     foreign key (Id_mat)
     references MATERIEL (Id_mat);

alter table Loue_mat add constraint FKLou_CLI_FK
     foreign key (Id_cli)
     references CLIENT (Id_cli);

alter table MATERIEL add constraint FKgere1_FK
     foreign key (Id_admin)
     references ADMINISTRATION (Id_admin);

alter table NETTOIE add constraint FKNET_TEC
     foreign key (Id_tech)
     references TECHNICIEN (Id_tech);

alter table NETTOIE add constraint FKNET_SEC_FK
     foreign key (Id_secteur)
     references SECTEUR (Id_secteur);

alter table participe add constraint FKpar_TOU
     foreign key (Id_tournoi)
     references TOURNOI (Id_tournoi);

alter table participe add constraint FKpar_EQU_FK
     foreign key (Id_equipe)
     references EQUIPE (Id_equipe);

-- Not implemented
-- alter table PERSONNE add constraint ID_PERSONNE_CHK
--     check(exists(select * from Prenom
--                  where Prenom.Id_Pers = Id_Pers)); 

-- alter table PERSONNE add constraint LSTONE_PERSONNE
--      check(STAFF is not null or CLIENT is not null); 

alter table peut_faire add constraint FKpeu_TYP
     foreign key (Id_type_acti)
     references TYPE_ACTI (Id_type_acti);

alter table peut_faire add constraint FKpeu_ANI_FK
     foreign key (Id_anim)
     references ANIMATEUR (Id_anim);

alter table Prenom add constraint FKPER_Pre
     foreign key (Id_Pers)
     references PERSONNE (Id_Pers);

-- alter table STAFF add constraint EXTONE_STAFF_1
--      check((Employe_ is not null and Prix_chef is null)
--            or (Employe_ is null and Prix_chef is not null)); 

-- alter table STAFF add constraint EXTONE_STAFF
--      check((TECHNICIEN is not null and ADMINISTRATION is null and CUISINIER is null and ANIMATEUR is null)
--            or (TECHNICIEN is null and ADMINISTRATION is not null and CUISINIER is null and ANIMATEUR is null)
--            or (TECHNICIEN is null and ADMINISTRATION is null and CUISINIER is not null and ANIMATEUR is null)
--            or (TECHNICIEN is null and ADMINISTRATION is null and CUISINIER is null and ANIMATEUR is not null)); 

alter table STAFF add constraint FKPER_STA_FK
     foreign key (Id_Pers)
     references PERSONNE (Id_Pers);

alter table STAFF add constraint FKdirige_FK
     foreign key (Employe_)
     references STAFF (Id_staff);

alter table TECHNICIEN add constraint FKSTA_TEC_FK
     foreign key (Id_staff)
     references STAFF (Id_staff);

-- Not implemented
-- alter table TOURNOI add constraint ID_TOURNOI_CHK
--     check(exists(select * from participe
--                  where participe.Id_tournoi = Id_tournoi)); 

alter table TOURNOI add constraint FKde_FK
     foreign key (Id_acti)
     references ACTIVITE (Id_acti);

-- Not implemented
-- alter table TYPE_ACTI add constraint ID_TYPE_ACTI_CHK
--     check(exists(select * from peut_faire
--                  where peut_faire.Id_type_acti = Id_type_acti)); 


-- Index Section
-- _____________ 

create unique index ID_ACTIVITE_IND
     on ACTIVITE (Id_acti);

create index FKde__IND
     on ACTIVITE (Id_type_acti);

create index FKanime_IND
     on ACTIVITE (Id_anim);

create unique index ID_ADMINISTRATION_IND
     on ADMINISTRATION (Id_admin);

create unique index FKSTA_ADM_IND
     on ADMINISTRATION (Id_staff);

create unique index ID_ANIMATEUR_IND
     on ANIMATEUR (Id_anim);

create unique index FKSTA_ANI_IND
     on ANIMATEUR (Id_staff);

create unique index ID_CLIENT_IND
     on CLIENT (Id_cli);

create unique index FKPER_CLI_IND
     on CLIENT (Id_Pers);

create index FKfait_partie_IND
     on CLIENT (Id_equipe);

create unique index ID_cuisine_IND
     on cuisine (Id_emplacement, Id_tournoi, Id_cuis);

create index FKcui_TOU_IND
     on cuisine (Id_tournoi);

create index FKcui_CUI_IND
     on cuisine (Id_cuis);

create unique index ID_CUISINIER_IND
     on CUISINIER (Id_cuis);

create unique index FKSTA_CUI_IND
     on CUISINIER (Id_staff);

create unique index ID_EMPLACEMENT_IND
     on EMPLACEMENT (Id_emplacement);

create unique index ID_EQUIPE_IND
     on EQUIPE (Id_equipe);

create unique index ID_FICHE_COMPTA_IND
     on FICHE_COMPTA (Id_fiche_compta);

create index FKgere2_IND
     on FICHE_COMPTA (Id_admin);

create unique index ID_inscription_IND
     on inscription (Id_acti, Id_cli);

create index FKins_CLI_IND
     on inscription (Id_cli);

create unique index ID_loue_emplacement_IND
     on loue_emplacement (Id_emplacement, Id_cli);

create index FKlou_CLI_1_IND
     on loue_emplacement (Id_cli);

create unique index ID_Loue_mat_IND
     on Loue_mat (Id_mat, Id_cli);

create index FKLou_CLI_IND
     on Loue_mat (Id_cli);

create unique index ID_MATERIEL_IND
     on MATERIEL (Id_mat);

create index FKgere1_IND
     on MATERIEL (Id_admin);

create unique index ID_NETTOIE_IND
     on NETTOIE (Id_tech, Heure, Date_net);

create index FKNET_SEC_IND
     on NETTOIE (Id_secteur);

create unique index ID_participe_IND
     on participe (Id_tournoi, Id_equipe);

create index FKpar_EQU_IND
     on participe (Id_equipe);

create unique index ID_PERSONNE_IND
     on PERSONNE (Id_Pers);

create unique index ID_peut_faire_IND
     on peut_faire (Id_type_acti, Id_anim);

create index FKpeu_ANI_IND
     on peut_faire (Id_anim);

create unique index ID_Prenom_IND
     on Prenom (Id_Pers, Prenom);

create unique index ID_SECTEUR_IND
     on SECTEUR (Id_secteur);

create unique index ID_STAFF_IND
     on STAFF (Id_staff);

create unique index FKPER_STA_IND
     on STAFF (Id_Pers);

create index FKdirige_IND
     on STAFF (Employe_);

create unique index ID_TECHNICIEN_IND
     on TECHNICIEN (Id_tech);

create unique index FKSTA_TEC_IND
     on TECHNICIEN (Id_staff);

create unique index ID_TOURNOI_IND
     on TOURNOI (Id_tournoi);

create unique index FKde_IND
     on TOURNOI (Id_acti);

create unique index ID_TYPE_ACTI_IND
     on TYPE_ACTI (Id_type_acti);

-- Dump Section
INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('Doe', 25, '$2b$12$57ToY5hwTRn.nbMcQ95XQuRG0UsbL4va2rb5.xFYU.lR4HNpH.rnW');
INSERT INTO Prenom (Prenom, Id_Pers) VALUES ('John', 1);
INSERT INTO CLIENT (Id_Pers, Pays, Code_postal, Ville, Numero_de_maison, Con_Email, Con_Telephone) VALUES (1, 'France', 75000, 'Paris', 1, 'John.Doe@gmail.com', 0600000000);

INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('Johnson', 20, '$2b$12$Ki8MD5hrvVyZi601OrM5ROuSl0d7WfmsHA4Cv8UycvA.XWZylllb.');
INSERT INTO Prenom (Prenom, Id_Pers) VALUES ('Jack', 2);
INSERT INTO CLIENT (Id_Pers, Pays, Code_postal, Ville, Numero_de_maison, Con_Email, Con_Telephone) VALUES (2, 'France', 75000, 'Paris', 2, 'Jack.Johnson@gmail.com', 0600000001);

INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('Daniel', 6, '$2b$12$FS4buiVtAPmHbMUdu1fNBOQRWKiush7NBUp3dhf0oUOVRWXYxGcjK');
INSERT INTO Prenom (Prenom, Id_pers) VALUES ('David', 3);
INSERT INTO CLIENT (Id_Pers, Pays, Code_postal, Ville, Numero_de_maison, Con_Email, Con_Telephone) VALUES (3, 'France', 75000, 'Paris', 3, 'boutchou@gmail.com', 0600000002);

INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('Merton', 30, '$2b$12$qVlioM4Yc.UMuDIRuR/Up.tRFQVfAb4oBVjwN9LFhCHQ6/EVO5IKi');
INSERT INTO Prenom (Prenom, Id_pers) VALUES ('Angela', 4);
INSERT INTO CLIENT (Id_Pers, Pays, Code_postal, Ville, Numero_de_maison, Con_Email, Con_Telephone) VALUES (4, 'France', 75000, 'Paris', 4, 'angela.merton@gmail.com', 0600000003);

INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('Bouffioux', 19, '$2b$12$xTLAckXQcNvVnNuM3B1TSurI5e8nNfgWr9G4gu.P7Oag6mtt9LGVK');
INSERT INTO Prenom (Prenom, Id_pers) VALUES ('Corentin', 5);
INSERT INTO STAFF (Id_Pers, Prix) VALUES (5, 1700);
INSERT INTO ANIMATEUR (Id_staff) VALUES (1);

INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('Elice', 19, '$2b$12$X5JRqLcjlN5xXaW04OB61.c.LcpN.NWhWqQao0peSBsDJn2P.VJmC');
INSERT INTO Prenom (Prenom, Id_pers) VALUES ('Simon', 6);
INSERT INTO STAFF (Id_Pers, Prix) VALUES (6, 2200);
INSERT INTO CUISINIER (Id_staff) VALUES (2);

INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('VV', 19, '$2b$12$t6YGDhFi/3LNfUH973DX5OKQhR/QB2YM6Is2Uc3TIzzdhElqCnL5u');
INSERT INTO Prenom (Prenom, Id_pers) VALUES ('Alexis', 7);
INSERT INTO STAFF (Id_Pers, Prix) VALUES (7, 1700);
INSERT INTO ADMINISTRATION (Id_staff) VALUES (3);

INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('Morg', 26, '$2b$12$Zqdaf/C3F3o6/1QEJ2pnA.CLghaj2td6vMvMwGvQ1LPzY.UliO2eS');
INSERT INTO Prenom (Prenom, Id_pers) VALUES ('Morgan', 8);
INSERT INTO STAFF (Id_Pers, Prix) VALUES (8, 2000);
INSERT INTO TECHNICIEN (Id_staff) VALUES (4);

INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('Bernagou', 19, '$2b$12$fQN.wGB5NdJm5tK782YNZeh4G1nHdXm0yqdKRHre0C5XTSHTtLYye');
INSERT INTO Prenom (Prenom, Id_pers) VALUES ('Esteban', 9);
INSERT INTO STAFF (Id_Pers, Prix ,Prix_chef) VALUES (9, 1700, 1000);
INSERT INTO ANIMATEUR (Id_staff) VALUES (5);

INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES ('Leco', 27, '$2b$12$SAQfBRo8tMIAweh/twFzNONf0hmZN4pWF4qBl5Th/qk2IYg87ucyG');
INSERT INTO Prenom (Prenom, Id_pers) VALUES ('Clement', 10);
INSERT INTO STAFF (Id_Pers, Prix) VALUES (10, 1700);
INSERT INTO ANIMATEUR (Id_staff) VALUES (6);

INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (10, 0, 5, 'Basketball');
INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (15, 0, 3, 'Football');
INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (10, 130, 8, 'Volleyball');
INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (40, 0, 18, 'Spa');
INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (40, 140, 15, 'Ski-Nautique');
INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (10, 0, 4, 'Badminton');
INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (20, 130, 10, 'Escalade');
INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (10, 0, 3, 'Mini-Golf');
INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (15, 0, 3, 'Club enfant');
INSERT INTO TYPE_ACTI (Prix, Taille_min_, Age_min, Nom) VALUES (70, 150, 15, 'Plongée');

INSERT INTO ACTIVITE (Date_acti, Heure, Lieu, Id_type_acti) VALUES ('2023-07-01', '10:00', 'Terrain de basket', 1);
INSERT INTO ACTIVITE (Date_acti, Heure, Lieu, Id_type_acti) VALUES ('2023-07-01', '14:00', 'Terrain de football', 2);
INSERT INTO ACTIVITE (Date_acti, Heure, Lieu, Id_type_acti) VALUES ('2023-07-02', '16:00', 'Terrain de volleyball', 3);

INSERT INTO TOURNOI (Date_tournoi, Heure, Lieu, Id_acti, Prix) VALUES ('2023-07-01', '10:00', 'Terrain de basket', 1, 10);
INSERT INTO TOURNOI (Date_tournoi, Heure, Lieu, Id_acti, Prix) VALUES ('2023-07-01', '14:00', 'Terrain de volleyball', 3, 10);

INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Ballon de foot', 'Sport', 8, 'Mitigé');
INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Raquette de bad', 'Sport', 15, 'Mitigé');
INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Baudrier', 'Sport', 20, 'Bon');
INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Volant', 'Sport', 5, 'Mitigé');
INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Cubs de golf', 'Sport', 15, 'Mitigé');
INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Balles de golf', 'Sport', 5, 'Mitigé');
INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Masque et tuba', 'Sport', 20, 'Très bon');
INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Raclettes', 'Entretien', 10, 'Mitigé');
INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Boite à outils', 'Entretien', 15, 'Très bon');
INSERT INTO MATERIEL (Nom, Type_mat, Prix, Etat) VALUES ('Kit survie', 'Santé', 30, 'Neuve');

INSERT INTO SECTEUR (Nom) VALUES ('Lac');
INSERT INTO SECTEUR (Nom) VALUES ('Plaine de jeu');
INSERT INTO SECTEUR (Nom) VALUES ('Piscine');
INSERT INTO SECTEUR (Nom) VALUES ('Douches publiques');
INSERT INTO SECTEUR (Nom) VALUES ('Spa');
INSERT INTO SECTEUR (Nom) VALUES ('Salle de sport');

INSERT INTO EMPLACEMENT(Type_emplacement, Occupation, Prix, bbq, nbr_places, acces_eau, Cuisinier) VALUES ('Tente', 0, 20, 1, 4, 1, 0);
INSERT INTO EMPLACEMENT(Type_emplacement, Occupation, Prix, bbq, nbr_places, acces_eau, Cuisinier) VALUES ('Caravane', 0, 30, 0, 4, 1, 0);
INSERT INTO EMPLACEMENT(Type_emplacement, Occupation, Prix, bbq, nbr_places, acces_eau, Cuisinier) VALUES ('Mobil-home', 0, 70, 1, 4, 1, 0);



-- Views Section

create VIEW view_Client AS
SELECT C.Id_cli, Pays, Code_postal, Ville, Numero_de_maison, I.Id_acti, E.Id_equipe, E.Nom AS "Equipe", E.Nbr_pers, E.Nbr_PersMax, P.Id_tournoi, Id_emplacement, PS.Nom, PS.age, Con_Email, Con_Telephone, LM.Id_mat, Date_loc
FROM CLIENT C
JOIN PERSONNE PS ON C.Id_Pers = PS.Id_Pers
LEFT JOIN inscription I ON C.Id_cli = I.Id_cli
LEFT JOIN ACTIVITE A ON I.Id_acti = A.Id_acti
LEFT JOIN EQUIPE E ON C.Id_equipe = E.Id_equipe
LEFT JOIN participe P ON E.Id_equipe = P.Id_equipe
LEFT JOIN TOURNOI T ON P.Id_tournoi = T.Id_tournoi
LEFT JOIN loue_emplacement L ON C.Id_cli = L.Id_cli
LEFT JOIN Loue_mat LM ON C.Id_cli = LM.Id_cli
LEFT JOIN MATERIEL M ON LM.Id_mat = M.Id_mat;

create VIEW view_Animateur_PossibleActivite AS
select S.Id_staff, PS.Nom, Age, S.Id_Pers, S.Prix, PF.Id_type_acti, TA.Nom as "Activite", TA.Prix as "Prix_acti", Taille_min_, Age_min
from STAFF S
JOIN PERSONNE PS ON PS.Id_Pers = S.Id_Pers
JOIN ANIMATEUR A ON A.Id_staff = S.Id_staff
LEFT JOIN peut_faire PF ON A.Id_anim = PF.Id_anim
LEFT JOIN TYPE_ACTI TA ON PF.Id_type_acti = TA.Id_type_acti;

create VIEW view_Animateur_Activite AS
SELECT S.Id_staff, PS.Nom, Age, S.Id_Pers, S.Prix AS "Salaire", Date_acti, Heure, Lieu,
       ACT.Id_type_acti, TA.Nom AS "Activite", TA.Prix AS "Prix_acti",
       Taille_min_, Age_min
FROM STAFF S
JOIN PERSONNE PS ON PS.Id_Pers = S.Id_Pers
JOIN ANIMATEUR A ON A.Id_staff = S.Id_staff
LEFT JOIN ACTIVITE ACT ON ACT.Id_anim = A.Id_anim
LEFT JOIN TYPE_ACTI TA ON TA.Id_type_acti = ACT.Id_type_acti;


create VIEW view_Employe_Technicien AS
select S.Id_staff, PS.Nom, Age, S.Id_Pers, Prix as "Salaire", T.Id_tech, Date_net, Heure, N.Id_secteur, SC.Nom as "Nom_secteur"
from STAFF S 
JOIN PERSONNE PS ON PS.Id_Pers = S.Id_Pers
JOIN TECHNICIEN T ON T.Id_staff = S.Id_staff
LEFT JOIN NETTOIE N ON T.Id_tech = N.Id_tech
LEFT JOIN SECTEUR SC ON N.Id_secteur = SC.Id_secteur;


create VIEW view_Chef AS
select S.Id_staff, Nom, Age, S.Id_Pers, Prix as "Salaire", Prix_chef as "Bonus"
from STAFF S, PERSONNE PS
where PS.Id_Pers = S.Id_Pers
and Prix_chef is not null;

create VIEW view_Cuisinier AS
select S.Id_staff, Nom, Age, S.Id_pers, Prix as "Salaire", Id_cuisine, Id_emplacement, Id_tournoi
from STAFF S
JOIN PERSONNE PS ON PS.Id_Pers = S.Id_Pers
JOIN CUISINIER C ON C.Id_staff = S.Id_staff
LEFT JOIN cuisine CU ON C.Id_cuis = CU.Id_cuis;

create VIEW view_Administration AS
select S.Id_staff, PS.Nom, Age, S.Id_pers, S.Prix as "Salaire", AD.ID_admin, Id_mat, M.Nom as "Materiel",Type_mat, M.Prix as "Prix_mat", Etat, Id_fiche_Compta, Date_fiche, Prix_total
from STAFF S 
JOIN PERSONNE PS ON PS.Id_Pers = S.Id_Pers
JOIN ADMINISTRATION AD ON AD.Id_staff = S.Id_staff
LEFT JOIN MATERIEL M ON AD.Id_admin = M.Id_admin
LEFT JOIN FICHE_COMPTA FC ON AD.Id_admin = FC.Id_admin;

create VIEW view_Comptabilite_EMPLACEMENT AS
SELECT Date_debut, LE.Id_emplacement, Prix, C.Id_cli, Nom
FROM CLIENT C
JOIN PERSONNE P ON C.Id_Pers = P.Id_pers
LEFT JOIN loue_emplacement LE ON LE.Id_cli = C.Id_cli
LEFT JOIN EMPLACEMENT E ON LE.Id_emplacement = E.Id_emplacement;

create VIEW view_Comptabilite_MATERIEL AS
select Date_loc, LM.Id_mat, M.Prix, C.Id_cli, P.Nom
from CLIENT C
JOIN PERSONNE P ON C.Id_Pers = P.Id_pers
LEFT JOIN Loue_mat LM ON LM.Id_cli = C.Id_cli
LEFT JOIN MATERIEL M ON LM.Id_mat = M.Id_mat;

create VIEW view_Comptabilite_STAFFChef AS
select Id_staff, Prix as "Salaire", Prix_chef as "Bonus"
from STAFF
where Prix_chef is not null;

create VIEW view_Comptabilite_STAFFEmploye AS
select Id_staff, Prix as "Salaire"
from STAFF
where Prix_chef is null;


-- Trigger Section

CREATE TRIGGER COMP_ACTI_ANIM
BEFORE UPDATE ON ACTIVITE
FOR EACH ROW
BEGIN
   if (
     not exists(
          select 1
          from ACTIVITE A, peut_faire p, ANIMATEUR N
          where new.Id_type_acti in(
               select Id_type_acti
               from peut_faire p
               where new.Id_anim = p.Id_anim
          ))
     )then SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vous n''avez pas les compétences requises.';
     end if;
END;

CREATE TRIGGER AGE_MIN
BEFORE INSERT ON inscription
FOR EACH ROW
BEGIN
   IF (
     (
        SELECT Age
        FROM PERSONNE P, CLIENT C
        WHERE new.id_cli = C.id_cli
        AND C.id_pers = P.id_pers
     ) <
     (
        SELECT Age_min
        FROM TYPE_ACTI T, ACTIVITE A
        WHERE new.id_acti = A.id_acti
        AND A.Id_type_acti = T.Id_type_acti
     )
   ) THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La personne n''a pas l''âge minimum requis.';
   END IF;
END;


CREATE TRIGGER CHEF_UNIQUE_PAR_SECTION
BEFORE UPDATE ON STAFF
FOR EACH ROW
BEGIN
    IF (new.Prix_chef IS NOT NULL) THEN
        IF (
            (SELECT COUNT(*) FROM STAFF S, TECHNICIEN T WHERE S.id_staff = T.id_staff AND S.Prix_chef IS NOT NULL) = 1
        ) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Il y a déjà un chef pour les techniciens, plus possible d''en insérer.';
        ELSEIF (
            (SELECT COUNT(*) FROM STAFF S, CUISINIER T WHERE S.id_staff = T.id_staff AND S.Prix_chef IS NOT NULL) = 1
        ) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Il y a déjà un chef pour les cuisiniers, plus possible d''en insérer.';
        ELSEIF (
            (SELECT COUNT(*) FROM STAFF S, ANIMATEUR T WHERE S.id_staff = T.id_staff AND S.Prix_chef IS NOT NULL) = 1
        ) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Il y a déjà un chef pour les animateurs, plus possible d''en insérer.';
        ELSEIF (
            (SELECT COUNT(*) FROM STAFF S, ADMINISTRATION T WHERE S.id_staff = T.id_staff AND S.Prix_chef IS NOT NULL) = 1
        ) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Il y a déjà un chef pour l''administration, plus possible d''en insérer.';
        END IF;
    END IF;
END;

create trigger CHEF_UNIQUE_PAR_SECTION
before update, insert on STAFF
for each row
when (new.Prix_chef is not null) --Nouveau chef
begin
     if(
          (1 = 
          ( 
          select
               (case when COUNT(*) > 0 THEN 1 ELSE 0 END) as is_that_type
          from STAFF S, TECHNICIEN T
          where new.id_staff = T.Id_staff
          )) --Fais partie de ce type de staff
          
          and -- verifier si déjà un chef dans ce secteur
          (1 = (
               select
                    (case when COUNT(*) > 0 THEN 1 ELSE 0 END) as already_one
               from STAFF S, TECHNICIEN T
               where S.id_staff = T.id_staff
               and S.Prix_chef is not null;
          ))
          )then SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT "Il y a déjà un chef pour les techniciens, plus possible d'en insérer.";
     
     ELSEIF(
          (1 = 
          ( 
          select
               (case when COUNT(*) > 0 THEN 1 ELSE 0 END) as is_that_type
          from STAFF S, CUISINIER T
          where new.id_staff = T.Id_staff
          )) --Fais partie de ce type de staff
          
          and -- verifier si déjà un chef dans ce secteur
          (1 = (
               select
                    (case when COUNT(*) > 0 THEN 1 ELSE 0 END) as already_one
               from STAFF S, CUISINIER T
               where S.id_staff = T.id_staff
               and S.Prix_chef is not null;
          ))
          )then SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT "Il y a déjà un chef pour les cuisiniers, plus possible d'en insérer.";
     
     ELSEIF(
          (1 = 
          ( 
          select
               (case when COUNT(*) > 0 THEN 1 ELSE 0 END) as is_that_type
          from STAFF S, ANIMATEUR T
          where new.id_staff = T.Id_staff
          )) --Fais partie de ce type de staff
          
          and -- verifier si déjà un chef dans ce secteur
          (1 = (
               select
                    (case when COUNT(*) > 0 THEN 1 ELSE 0 END) as already_one
               from STAFF S, ANIMATEUR T
               where S.id_staff = T.id_staff
               and S.Prix_chef is not null;
          ))
          )then SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT "Il y a déjà un chef pour les animateurs, plus possible d'en insérer.";
     

     if(
          (1 = 
          ( 
          select
               (case when COUNT(*) > 0 THEN 1 ELSE 0 END) as is_that_type
          from STAFF S, ADMINISTRATION T
          where new.id_staff = T.Id_staff
          )) --Fais partie de ce type de staff
          
          and -- verifier si déjà un chef dans ce secteur
          (1 = (
               select
                    (case when COUNT(*) > 0 THEN 1 ELSE 0 END) as already_one
               from STAFF S, ADMINISTRATION T
               where S.id_staff = T.id_staff
               and S.Prix_chef is not null;
          ))
          )then SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT "Il y a déjà un chef pour l'administration, plus possible d'en insérer.";
     
     end if;
end;

CREATE TRIGGER CHEF_UNIQUE_PAR_SECTION_2
BEFORE UPDATE ON STAFF
FOR EACH ROW
when (new.Prix_chef IS NOT NULL)
BEGIN
        IF (
            (SELECT COUNT(*) FROM STAFF S, TECHNICIEN T WHERE new.id_staff = T.Id_staff) = 1
            AND (SELECT COUNT(*) FROM STAFF S, TECHNICIEN T WHERE S.id_staff = T.id_staff AND S.Prix_chef IS NOT NULL) >0
        ) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Il y a déjà un chef pour les techniciens, plus possible d''en insérer.';
        ELSEIF (
            (SELECT COUNT(*) FROM STAFF S, CUISINIER T WHERE new.id_staff = T.Id_staff) = 1
            AND (SELECT COUNT(*) FROM STAFF S, CUISINIER T WHERE S.id_staff = T.id_staff AND S.Prix_chef IS NOT NULL) >0
        ) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Il y a déjà un chef pour les cuisiniers, plus possible d''en insérer.';
        ELSEIF (
            (SELECT COUNT(*) FROM STAFF S, ANIMATEUR T WHERE new.id_staff = T.Id_staff) = 1
            AND (SELECT COUNT(*) FROM STAFF S, ANIMATEUR T WHERE S.id_staff = T.id_staff AND S.Prix_chef IS NOT NULL) = 1
        ) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Il y a déjà un chef pour les animateurs, plus possible d''en insérer.';
        ELSEIF (
            (SELECT COUNT(*) FROM STAFF S, ADMINISTRATION T WHERE new.id_staff = T.Id_staff) = 1
            AND (SELECT COUNT(*) FROM STAFF S, ADMINISTRATION T WHERE S.id_staff = T.id_staff AND S.Prix_chef IS NOT NULL) >0
        ) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Il y a déjà un chef pour l''administration, plus possible d''en insérer.';
        END IF;
END;