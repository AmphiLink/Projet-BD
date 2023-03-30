-- *********************************************
-- * SQL MySQL generation                      
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Thu Mar 30 18:37:04 2023 
-- * LUN file: C:\Users\esteb\OneDrive\Bureau\Unif\2 ème année\Q2\BD 2\Projet-BD\Schémas\Camping-era.lun 
-- * Schema: code ddl/1-1-1 
-- ********************************************* 


-- Database Section
-- ________________ 

create database code ddl;
use code ddl;


-- Tables Section
-- _____________ 

create table ACTIVITE (
     Id_acti int not null,
     Date date not null,
     Heure varchar(250) not null,
     Lieu varchar(250) not null,
     Id_type_acti int not null,
     Id_anim int not null,
     constraint ID_ACTIVITE_ID primary key (Id_acti));

create table ADMINISTRATION (
     Id_admin int not null,
     Id_staff int not null,
     constraint ID_ADMINISTRATION_ID primary key (Id_admin),
     constraint FKSTA_ADM_ID unique (Id_staff));

create table ANIMATEUR (
     Id_anim int not null,
     Id_staff int not null,
     constraint ID_ANIMATEUR_ID primary key (Id_anim),
     constraint FKSTA_ANI_ID unique (Id_staff));

create table CLIENT (
     Id_cli int not null,
     Id_Pers int not null,
     Pays varchar(250) not null,
     Code_postal int not null,
     Ville varchar(250) not null,
     Numero_de_maison int not null,
     Con_Email varchar(250) not null,
     Con_Telephone int not null,
     Id_equipe int,
     constraint ID_CLIENT_ID primary key (Id_cli),
     constraint FKPER_CLI_ID unique (Id_Pers));

create table COMPTA_TOURNOI_VIEW (
     Id_feuille_compta char(1) not null,
     Prix_tournoi char(1) not null,
     Prix_staff char(1) not null,
     Prix_materiel char(1) not null,
     Prix_acti char(1) not null,
     constraint ID_COMPTA_TOURNOI_VIEW_ID primary key (Id_feuille_compta));

create table cuisine (
     Id_cuis int not null,
     Id_emplacement int not null,
     Id_tournoi int not null,
     constraint ID_cuisine_ID primary key (Id_emplacement, Id_tournoi, Id_cuis));

create table CUISINIER (
     Id_cuis int not null,
     Id_staff int not null,
     constraint ID_CUISINIER_ID primary key (Id_cuis),
     constraint FKSTA_CUI_ID unique (Id_staff));

create table EMPLACEMENT (
     Id_emplacement int not null,
     Type varchar(250) not null,
     Occupation char not null,
     Prix float(1) not null,
     bbq char not null,
     nbr_places int not null,
     acces_eau char not null,
     constraint ID_EMPLACEMENT_ID primary key (Id_emplacement));

create table FICHE_COMPTA (
     Id_fiche_compta int not null,
     Date date not null,
     Prix_total float(1) not null,
     constraint ID_FICHE_COMPTA_ID primary key (Id_fiche_compta));

create table EQUIPE (
     Id_equipe int not null,
     Nom varchar(250) not null,
     Nbr_pers int not null,
     constraint ID_EQUIPE_ID primary key (Id_equipe));

create table MATERIEL (
     Id_mat int not null,
     Nom varchar(250) not null,
     Type varchar(250) not null,
     Prix int not null,
     Etat varchar(250) not null,
     constraint ID_MATERIEL_ID primary key (Id_mat));

create table PERSONNE (
     Nom varchar(250) not null,
     Age int not null,
     Id_Pers int not null,
     STAFF int,
     CLIENT int,
     constraint ID_PERSONNE_ID primary key (Id_Pers));

create table SECTEUR (
     Id_secteur int not null,
     Nom varchar(250) not null,
     constraint ID_SECTEUR_ID primary key (Id_secteur));

create table STAFF (
     Id_staff int not null,
     Id_Pers int not null,
     Prix float(1) not null,
     Prix_chef float(1),
     TECHNICIEN int,
     CUISINIER int,
     ANIMATEUR int,
     ADMINISTRATION int,
     Chef_ int,
     constraint ID_STAFF_ID primary key (Id_staff),
     constraint FKPER_STA_ID unique (Id_Pers));

create table TECHNICIEN (
     Id_tech int not null,
     Id_staff int not null,
     constraint ID_TECHNICIEN_ID primary key (Id_tech),
     constraint FKSTA_TEC_ID unique (Id_staff));

create table TOURNOI (
     Id_tournoi int not null,
     Id_acti int not null,
     Date date not null,
     Lieu varchar(250) not null,
     Prix float(1) not null,
     constraint ID_TOURNOI_ID primary key (Id_tournoi),
     constraint FKde_ID unique (Id_acti));

create table TYPE_ACTI (
     Id_type_acti int not null,
     Prix float(1) not null,
     Taille_min_ int not null comment 'en cm',
     Age_min int not null,
     Nom varchar(250) not null,
     constraint ID_TYPE_ACTI_ID primary key (Id_type_acti));

create table gere (
     Id_admin int not null,
     Type_de_Gestion_1__1 int,
     Type_de_Gestion_1_ int,
     constraint ID_gere_1_ID primary key (Id_admin, Type_de_Gestion_1_),
     constraint ID_gere_ID primary key (Id_admin, Type_de_Gestion_1__1));

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

create table NETTOIE (
     Id_tech int not null,
     Date date not null,
     Heure varchar(250) not null,
     Id_secteur int not null,
     constraint ID_NETTOIE_ID primary key (Id_tech, Heure, Date));

create table participe (
     Id_equipe int not null,
     Id_tournoi int not null,
     constraint ID_participe_ID primary key (Id_tournoi, Id_equipe));

create table peut_faire (
     Id_anim int not null,
     Id_type_acti int not null,
     constraint ID_peut_faire_ID primary key (Id_type_acti, Id_anim));

create table Prenom (
     Id_Pers int not null,
     Prenom varchar(250) not null,
     constraint ID_Prenom_ID primary key (Id_Pers, Prenom));


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
-- alter table FICHE_COMPTA add constraint ID_FICHE_COMPTA_CHK
--     check(exists(select * from gere
--                  where gere.Type_de_Gestion_1_ = Id_fiche_compta)); 

-- Not implemented
-- alter table EQUIPE add constraint ID_EQUIPE_CHK
--     check(exists(select * from CLIENT
--                  where CLIENT.Id_equipe = Id_equipe)); 

-- Not implemented
-- alter table MATERIEL add constraint ID_MATERIEL_CHK
--     check(exists(select * from gere
--                  where gere.Type_de_Gestion_1__1 = Id_mat)); 

-- Not implemented
-- alter table PERSONNE add constraint ID_PERSONNE_CHK
--     check(exists(select * from Prenom
--                  where Prenom.Id_Pers = Id_Pers)); 

alter table PERSONNE add constraint LSTONE_PERSONNE
     check(STAFF is not null or CLIENT is not null); 

alter table STAFF add constraint EXTONE_STAFF_1
     check((Prix_chef is not null)); 

alter table STAFF add constraint EXTONE_STAFF
     check((TECHNICIEN is not null and ADMINISTRATION is null and CUISINIER is null and ANIMATEUR is null)
           or (TECHNICIEN is null and ADMINISTRATION is not null and CUISINIER is null and ANIMATEUR is null)
           or (TECHNICIEN is null and ADMINISTRATION is null and CUISINIER is not null and ANIMATEUR is null)
           or (TECHNICIEN is null and ADMINISTRATION is null and CUISINIER is null and ANIMATEUR is not null)); 

alter table STAFF add constraint FKPER_STA_FK
     foreign key (Id_Pers)
     references PERSONNE (Id_Pers);

alter table STAFF add constraint FKdirige_FK
     foreign key (Chef_)
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

alter table gere add constraint EXTONE_gere
     check((Type_de_Gestion_1__1 is not null and Type_de_Gestion_1_ is null)
           or (Type_de_Gestion_1__1 is null and Type_de_Gestion_1_ is not null)); 

alter table gere add constraint FKType_de_Gestion2_FK
     foreign key (Type_de_Gestion_1_)
     references FICHE_COMPTA (Id_fiche_compta);

alter table gere add constraint FKType_de_Gestion1_FK
     foreign key (Type_de_Gestion_1__1)
     references MATERIEL (Id_mat);

alter table gere add constraint FKger_ADM
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

alter table peut_faire add constraint FKpeu_TYP
     foreign key (Id_type_acti)
     references TYPE_ACTI (Id_type_acti);

alter table peut_faire add constraint FKpeu_ANI_FK
     foreign key (Id_anim)
     references ANIMATEUR (Id_anim);

alter table Prenom add constraint FKPER_Pre
     foreign key (Id_Pers)
     references PERSONNE (Id_Pers);


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

create unique index ID_COMPTA_TOURNOI_VIEW_IND
     on COMPTA_TOURNOI_VIEW (Id_feuille_compta);

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

create unique index ID_FICHE_COMPTA_IND
     on FICHE_COMPTA (Id_fiche_compta);

create unique index ID_EQUIPE_IND
     on EQUIPE (Id_equipe);

create unique index ID_MATERIEL_IND
     on MATERIEL (Id_mat);

create unique index ID_PERSONNE_IND
     on PERSONNE (Id_Pers);

create unique index ID_SECTEUR_IND
     on SECTEUR (Id_secteur);

create unique index ID_STAFF_IND
     on STAFF (Id_staff);

create unique index FKPER_STA_IND
     on STAFF (Id_Pers);

create index FKdirige_IND
     on STAFF (Chef_);

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

create unique index ID_gere_1_IND
     on gere (Id_admin, Type_de_Gestion_1_);

create unique index ID_gere_IND
     on gere (Id_admin, Type_de_Gestion_1__1);

create index FKType_de_Gestion2_IND
     on gere (Type_de_Gestion_1_);

create index FKType_de_Gestion1_IND
     on gere (Type_de_Gestion_1__1);

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

create unique index ID_NETTOIE_IND
     on NETTOIE (Id_tech, Heure, Date);

create index FKNET_SEC_IND
     on NETTOIE (Id_secteur);

create unique index ID_participe_IND
     on participe (Id_tournoi, Id_equipe);

create index FKpar_EQU_IND
     on participe (Id_equipe);

create unique index ID_peut_faire_IND
     on peut_faire (Id_type_acti, Id_anim);

create index FKpeu_ANI_IND
     on peut_faire (Id_anim);

create unique index ID_Prenom_IND
     on Prenom (Id_Pers, Prenom);

