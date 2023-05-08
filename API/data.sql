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
     constraint ID_EQUIPE_ID primary key (Id_equipe));

create table FICHE_COMPTA (
     Id_fiche_compta int not null AUTO_INCREMENT,
     Date_fiche date not null,
     Prix_total float(1) not null,
     Id_admin int not null,   
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
     Age int,
     Id_Pers int not null AUTO_INCREMENT,
     Mot_de_passe varchar(250),
     STAFF int,
     CLIENT int,
     constraint ID_PERSONNE_ID primary key (Id_Pers));

create table peut_faire (
     Id_anim int not null,
     Id_type_acti int not null,
     constraint ID_peut_faire_ID primary key (Id_type_acti, Id_anim));

create table Prenom (
     Id_Pers int not null,
     Prenom varchar(250) null,
     constraint ID_Prenom_ID primary key (Id_Pers));

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

--- Views Section

create VIEW view_Client AS
select C.Id_cli as "Id du client", Pays, Code_postal, Ville, Numero_de_maison, I.Id_acti, E.Id_equipe, E.Nom as "Nom de l'équipe", Id_Tournoi, Id_emplacement 
from CLIENT C, inscription I, ACTIVITE A, loue_emplacement L, EQUIPE E, participe P
where C.Id_cli = I.Id_cli
and I.Id_acti = A.Id_acti
and C.Id_cli = L.Id_cli
and C.Id_equipe = E.Id_equipe
and E.Id_equipe = P.Id_equipe;

create VIEW view_Chef_Animateur AS
select S.Id_staff, Nom, Prenom, Age, S.Id_pers, Prix as "Salaire", Mot_de_passe
from Staff S, Prenom P, PERSONNE PS
where PS.Id_Pers = P.Id_Pers
and PS.Id_Pers = S.Id_Pers
and Prix_chef != null
and ANIMATEUR != null;

create VIEW view_Animateur_PossibleActivite AS
select S.Id_staff, PS.Nom, Prenom, Age, S.Id_pers, S.Prix as "Salaire", Mot_de_passe, PF.Id_type_acti as "Type de l'activité", TA.Nom as "Nom de l'activité", TA.Prix, Taille_min_, Age_min
from Staff S, Prenom P, PERSONNE PS, ANIMATEUR A, peut_faire PF, TYPE_ACTI TA
where PS.Id_Pers = P.Id_Pers
and PS.Id_Pers = S.Id_Pers
and S.Id_staff = A.Id_anim
and A.Id_anim = PF.Id_anim
and TA.Id_type_acti = PF.Id_type_acti
and Prix_chef = null
and ANIMATEUR != null;

create VIEW view_Animateur_Activite AS
select S.Id_staff, PS.Nom, Prenom, Age, S.Id_pers, S.Prix as "Salaire", Mot_de_passe, Date_Acti as "Date", Heure, Lieu, PF.Id_type_acti, TA.Nom as "Nom de l'activité", TA.Prix "Prix de l'activité", Taille_min_ "Taille minimum", Age_min as "Age minimum"
from Staff S, Prenom P, PERSONNE PS, ANIMATEUR A, peut_faire PF, TYPE_ACTI TA, ACTIVITE ACT
where PS.Id_Pers = P.Id_Pers
and PS.Id_Pers = S.Id_Pers
and S.Id_staff = A.Id_anim
and A.Id_anim = PF.Id_anim
and ACT.Id_anim = A.Id_anim
and TA.Id_type_acti = ACT.Id_type_acti
and Prix_chef = null
and ANIMATEUR != null;

create VIEW view_Chef_Technicien AS
select S.Id_staff, Nom, Prenom, Age, S.Id_pers, Prix as "Salaire", Mot_de_passe
from Staff S, Prenom P, PERSONNE PS
where PS.Id_Pers = P.Id_Pers
and PS.Id_Pers = S.Id_Pers
and Prix_chef != null
and TECHNICIEN != null;

create VIEW view_Employé_Technicien AS
select S.Id_staff, PS.Nom as "Nom", Prenom, Age, S.Id_pers, Prix as "Salaire", Mot_de_passe, T.Id_tech, Date_Net, Heure, N.Id_secteur, SC.Nom as "Nom du Secteur"
from Staff S, Prenom P, PERSONNE PS, TECHNICIEN T, NETTOIE N, SECTEUR SC
where PS.Id_Pers = P.Id_Pers
and PS.Id_Pers = S.Id_Pers
and S.Id_staff = T.Id_staff
and T.Id_tech = N.Id_tech
and N.Id_secteur = SC.Id_secteur  
and Prix_chef = null
and TECHNICIEN != null;

create VIEW view_Chef_Cuisinier AS
select S.Id_staff, Nom, Prenom, Age, S.Id_pers, Prix as "Salaire", Mot_de_passe
from Staff S, Prenom P, PERSONNE PS
where PS.Id_Pers = P.Id_Pers
and PS.Id_Pers = S.Id_Pers
and Prix_chef != null
and CUISINIER != null;

create VIEW view_Cuisinier AS
select S.Id_staff, Nom, Prenom, Age, S.Id_pers, Prix as "Salaire", Mot_de_passe, Id_cuisine,  Id_emplacement, Id_tournoi
from Staff S, Prenom P, PERSONNE PS, CUISINIER C , cuisine CU
where PS.Id_Pers = P.Id_Pers
and PS.Id_Pers = S.Id_Pers
and S.Id_staff = C.Id_staff
and CU.Id_cuis = C.Id_cuis
and Prix_chef = null
and CUISINIER != null;

create VIEW view_Administration AS
select S.Id_staff, PS.Nom, Prenom, Age, S.Id_pers, S.Prix as "Salaire", Mot_de_passe, AD.ID_admin, Id_mat, M.Nom as "Nom du matériel",Type_Mat as "Type du matériel", M.Prix as "Prix du matériel", Etat, Id_fiche_Compta, Date_Fiche as "date de la fiche", Prix_total as "Prix total de la fiche"
from Staff S, Prenom P, PERSONNE PS, ADMINISTRATION AD, MATERIEL M, FICHE_COMPTA FC
where PS.Id_Pers = P.Id_Pers
and PS.Id_Pers = S.Id_Pers
and AD.Id_admin = FC.Id_admin
and AD.Id_admin = M.Id_admin
and ADMINISTRATION != null;

create VIEW view_Comptabilité_EMPLACEMENT AS
select Date_debut, LE.Id_emplacement, Prix, C.Id_cli as "Id Client", Nom, Prenom 
from loue_emplacement LE, EMPLACEMENT E, CLIENT C, PERSONNE P, PRENOM PR
where LE.id_emplacement = E.Id_emplacement
and LE.Id_cli = C.Id_cli
and C.Id_Pers = P.Id_pers
and PR.Id_Pers = P.Id_pers;

create VIEW view_Comptabilité_MATERIEL AS
select Date_loc as "Date de location", LM.Id_mat, Prix, C.Id_cli as "Id Client", P.Nom, Prenom 
from Loue_mat LM, MATERIEL M, CLIENT C, PERSONNE P, PRENOM PR
where M.Id_mat = LM.Id_mat
and LM.Id_cli = C.Id_cli
and C.Id_Pers = P.Id_pers
and PR.Id_Pers = P.Id_pers;

create VIEW view_Comptabilité_Emplacement AS
select Date_debut, LE.Id_emplacement, Prix, C.Id_cli as "Id Client", Nom, Prenom 
from loue_emplacement LE, EMPLACEMENT E, CLIENT C, PERSONNE P, PRENOM PR
where LE.id_emplacement = E.Id_emplacement
and LE.Id_cli = C.Id_cli
and C.Id_Pers = P.Id_pers
and PR.Id_Pers = P.Id_pers;

create VIEW view_Comptabilité_STAFFChef AS
select Id_staff, Prix as "Salaire"
from Staff
where Prix_chef != null
and Employe_ = null;

create VIEW view_Comptabilité_STAFFEmploye AS
select Id_staff, Prix as "Salaire"
from Staff
where Prix_chef = null
and Employe_ != null;