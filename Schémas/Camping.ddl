-- *********************************************
-- * SQL MySQL generation                      
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Thu Mar 30 15:54:18 2023 
-- * LUN file: C:\Users\esteb\OneDrive\Bureau\Unif\2 ème année\Q2\BD 2\Projet-BD\Schémas\Camping-era.lun 
-- * Schema: camping_ddl/1-1-1 
-- ********************************************* 


-- Database Section
-- ________________ 

create database camping_ddl;
use camping_ddl;


-- Tables Section
-- _____________ 

create table ACTIVITES (
     Id_acti char(1) not null,
     Date char(1) not null,
     Heure char(1) not null,
     Lieu char(1) not null,
     Type_acti varchar(1) not null,
     Id_Pers char(1) not null,
     constraint ID_ACTIVITES_ID primary key (Id_acti));

create table ADMINISTRATION (
     Id_Pers char(1) not null,
     Id_admin char(1) not null,
     constraint SID_ADMINISTRATION_ID unique (Id_admin),
     constraint FKSTA_ADM_ID primary key (Id_Pers));

create table ANIMATEUR (
     Id_Pers char(1) not null,
     Id_anim char(1) not null,
     constraint SID_ANIMATEUR_ID unique (Id_anim),
     constraint FKSTA_ANI_ID primary key (Id_Pers));

create table CLIENT (
     Id_Pers char(1) not null,
     Id_cli char(1) not null,
     Pays char(1) not null,
     Code_postal char(1) not null,
     Ville char(1) not null,
     Numero_de_maison char(1) not null,
     Con_Email char(1) not null,
     Con_Telephone char(1) not null,
     Id_equipe char(1),
     constraint SID_CLIENT_ID unique (Id_cli),
     constraint FKPER_CLI_ID primary key (Id_Pers));

create table COMPTA_TOURNOI_VIEW (
     Id_feuille_compta char(1) not null,
     Prix_tournoi char(1) not null,
     Prix_staff char(1) not null,
     Prix_materiel char(1) not null,
     Prix_acti char(1) not null,
     constraint ID_COMPTA_TOURNOI_VIEW_ID primary key (Id_feuille_compta));

create table cuisine_pour (
     Id_Pers char(1) not null,
     Id_emplacement char(1) not null,
     Id_tournoi char(1) not null,
     constraint ID_cuisine_pour_ID primary key (Id_emplacement, Id_tournoi, Id_Pers));

create table CUISINIER (
     Id_Pers char(1) not null,
     Id_cuis char(1) not null,
     constraint SID_CUISINIER_ID unique (Id_cuis),
     constraint FKSTA_CUI_ID primary key (Id_Pers));

create table EMPLACEMENT (
     Id_emplacement char(1) not null,
     Type char(1) not null,
     Occupation char not null,
     Prix int not null,
     bbq char not null,
     nbr_places int not null,
     acces_eau char not null,
     constraint ID_EMPLACEMENT_ID primary key (Id_emplacement));

create table EQUIPE (
     Id_equipe char(1) not null,
     Nom char(1) not null,
     Nbr_pers char(1) not null,
     constraint ID_EQUIPE_ID primary key (Id_equipe));

create table gere (
     Id_Pers char(1) not null,
     Id_mat char(1) not null,
     constraint ID_gere_ID primary key (Id_Pers, Id_mat));

create table inscription (
     Id_acti char(1) not null,
     Id_Pers char(1) not null,
     constraint ID_inscription_ID primary key (Id_acti, Id_Pers));

create table loue_emplacement (
     Id_Pers char(1) not null,
     Id_emplacement char(1) not null,
     Date_debut char(1) not null,
     Date_fin char(1) not null,
     constraint ID_loue_emplacement_ID primary key (Id_emplacement, Id_Pers));

create table Loue_mat (
     Id_Pers char(1) not null,
     Id_mat char(1) not null,
     Date_loc char(1) not null,
     constraint ID_Loue_mat_ID primary key (Id_mat, Id_Pers));

create table MATERIEL (
     Id_mat char(1) not null,
     Nom char(1) not null,
     Type char(1) not null,
     Prix char(1) not null,
     Etat char(1) not null,
     constraint ID_MATERIEL_ID primary key (Id_mat));

create table NETTOIE (
     Id_Pers char(1) not null,
     Date char(1) not null,
     Heure char(1) not null,
     Id_secteur char(1) not null,
     constraint ID_NETTOIE_ID primary key (Id_Pers, Heure, Date));

create table participe (
     Id_equipe char(1) not null,
     Id_tournoi char(1) not null,
     constraint ID_participe_ID primary key (Id_tournoi, Id_equipe));

create table PERSONNE (
     Nom char(1) not null,
     Age char(1) not null,
     Id_Pers char(1) not null,
     STAFF char(1),
     CLIENT char(1),
     constraint ID_PERSONNE_ID primary key (Id_Pers));

create table peut_faire (
     Id_Pers char(1) not null,
     Type_acti varchar(1) not null,
     constraint ID_peut_faire_ID primary key (Type_acti, Id_Pers));

create table Prenom (
     Id_Pers char(1) not null,
     Prenom char(1) not null,
     constraint ID_Prenom_ID primary key (Id_Pers, Prenom));

create table SECTEUR (
     Id_secteur char(1) not null,
     Nom char(1) not null,
     constraint ID_SECTEUR_ID primary key (Id_secteur));

create table STAFF (
     Id_Pers char(1) not null,
     Id_staff char(1) not null,
     Prix char(1) not null,
     Prix_chef char(1),
     Chef_ char(1),
     TECHNICIEN char(1),
     CUISINIER char(1),
     ANIMATEUR char(1),
     ADMINISTRATION char(1),
     constraint SID_STAFF_ID unique (Id_staff),
     constraint FKPER_STA_ID primary key (Id_Pers));

create table TECHNICIEN (
     Id_Pers char(1) not null,
     Id_tech char(1) not null,
     constraint SID_TECHNICIEN_ID unique (Id_tech),
     constraint FKSTA_TEC_ID primary key (Id_Pers));

create table TOURNOI (
     Id_tournoi char(1) not null,
     Id_acti char(1) not null,
     Date char(1) not null,
     Lieu char(1) not null,
     Prix char(1) not null,
     constraint ID_TOURNOI_ID primary key (Id_tournoi),
     constraint FKde_ID unique (Id_acti));

create table TYPE_ACTI (
     Type_acti varchar(1) not null,
     Prix int not null,
     Taille_min_ int not null comment 'en cm',
     Age_min int not null,
     Nom varchar(1) not null,
     constraint ID_TYPE_ACTI_ID primary key (Type_acti));


-- Constraints Section
-- ___________________ 

alter table ACTIVITES add constraint FKde__FK
     foreign key (Type_acti)
     references TYPE_ACTI (Type_acti);

alter table ACTIVITES add constraint FKanime_FK
     foreign key (Id_Pers)
     references ANIMATEUR (Id_Pers);

alter table ADMINISTRATION add constraint FKSTA_ADM_FK
     foreign key (Id_Pers)
     references STAFF (Id_Pers);

-- Not implemented
-- alter table ANIMATEUR add constraint FKSTA_ANI_CHK
--     check(exists(select * from peut_faire
--                  where peut_faire.Id_Pers = Id_Pers)); 

alter table ANIMATEUR add constraint FKSTA_ANI_FK
     foreign key (Id_Pers)
     references STAFF (Id_Pers);

-- Not implemented
-- alter table CLIENT add constraint FKPER_CLI_CHK
--     check(exists(select * from loue_emplacement
--                  where loue_emplacement.Id_Pers = Id_Pers)); 

alter table CLIENT add constraint FKPER_CLI_FK
     foreign key (Id_Pers)
     references PERSONNE (Id_Pers);

alter table CLIENT add constraint FKfait_partie_FK
     foreign key (Id_equipe)
     references EQUIPE (Id_equipe);

alter table cuisine_pour add constraint FKcui_TOU_FK
     foreign key (Id_tournoi)
     references TOURNOI (Id_tournoi);

alter table cuisine_pour add constraint FKcui_EMP
     foreign key (Id_emplacement)
     references EMPLACEMENT (Id_emplacement);

alter table cuisine_pour add constraint FKcui_CUI_FK
     foreign key (Id_Pers)
     references CUISINIER (Id_Pers);

alter table CUISINIER add constraint FKSTA_CUI_FK
     foreign key (Id_Pers)
     references STAFF (Id_Pers);

alter table gere add constraint FKger_MAT_FK
     foreign key (Id_mat)
     references MATERIEL (Id_mat);

alter table gere add constraint FKger_ADM
     foreign key (Id_Pers)
     references ADMINISTRATION (Id_Pers);

alter table inscription add constraint FKins_CLI_FK
     foreign key (Id_Pers)
     references CLIENT (Id_Pers);

alter table inscription add constraint FKins_ACT
     foreign key (Id_acti)
     references ACTIVITES (Id_acti);

alter table loue_emplacement add constraint FKlou_EMP
     foreign key (Id_emplacement)
     references EMPLACEMENT (Id_emplacement);

alter table loue_emplacement add constraint FKlou_CLI_1_FK
     foreign key (Id_Pers)
     references CLIENT (Id_Pers);

alter table Loue_mat add constraint FKLou_MAT
     foreign key (Id_mat)
     references MATERIEL (Id_mat);

alter table Loue_mat add constraint FKLou_CLI_FK
     foreign key (Id_Pers)
     references CLIENT (Id_Pers);

alter table NETTOIE add constraint FKNET_SEC_FK
     foreign key (Id_secteur)
     references SECTEUR (Id_secteur);

alter table NETTOIE add constraint FKNET_TEC
     foreign key (Id_Pers)
     references TECHNICIEN (Id_Pers);

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

alter table PERSONNE add constraint LSTONE_PERSONNE
     check(STAFF is not null or CLIENT is not null); 

alter table peut_faire add constraint FKpeu_TYP
     foreign key (Type_acti)
     references TYPE_ACTI (Type_acti);

alter table peut_faire add constraint FKpeu_ANI_FK
     foreign key (Id_Pers)
     references ANIMATEUR (Id_Pers);

alter table Prenom add constraint FKPER_Pre
     foreign key (Id_Pers)
     references PERSONNE (Id_Pers);

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
     references STAFF (Id_Pers);

alter table TECHNICIEN add constraint FKSTA_TEC_FK
     foreign key (Id_Pers)
     references STAFF (Id_Pers);

-- Not implemented
-- alter table TOURNOI add constraint ID_TOURNOI_CHK
--     check(exists(select * from participe
--                  where participe.Id_tournoi = Id_tournoi)); 

alter table TOURNOI add constraint FKde_FK
     foreign key (Id_acti)
     references ACTIVITES (Id_acti);

-- Not implemented
-- alter table TYPE_ACTI add constraint ID_TYPE_ACTI_CHK
--     check(exists(select * from peut_faire
--                  where peut_faire.Type_acti = Type_acti)); 


-- Index Section
-- _____________ 

create unique index ID_ACTIVITES_IND
     on ACTIVITES (Id_acti);

create index FKde__IND
     on ACTIVITES (Type_acti);

create index FKanime_IND
     on ACTIVITES (Id_Pers);

create unique index SID_ADMINISTRATION_IND
     on ADMINISTRATION (Id_admin);

create unique index FKSTA_ADM_IND
     on ADMINISTRATION (Id_Pers);

create unique index SID_ANIMATEUR_IND
     on ANIMATEUR (Id_anim);

create unique index FKSTA_ANI_IND
     on ANIMATEUR (Id_Pers);

create unique index SID_CLIENT_IND
     on CLIENT (Id_cli);

create unique index FKPER_CLI_IND
     on CLIENT (Id_Pers);

create index FKfait_partie_IND
     on CLIENT (Id_equipe);

create unique index ID_COMPTA_TOURNOI_VIEW_IND
     on COMPTA_TOURNOI_VIEW (Id_feuille_compta);

create unique index ID_cuisine_pour_IND
     on cuisine_pour (Id_emplacement, Id_tournoi, Id_Pers);

create index FKcui_TOU_IND
     on cuisine_pour (Id_tournoi);

create index FKcui_CUI_IND
     on cuisine_pour (Id_Pers);

create unique index SID_CUISINIER_IND
     on CUISINIER (Id_cuis);

create unique index FKSTA_CUI_IND
     on CUISINIER (Id_Pers);

create unique index ID_EMPLACEMENT_IND
     on EMPLACEMENT (Id_emplacement);

create unique index ID_EQUIPE_IND
     on EQUIPE (Id_equipe);

create unique index ID_gere_IND
     on gere (Id_Pers, Id_mat);

create index FKger_MAT_IND
     on gere (Id_mat);

create unique index ID_inscription_IND
     on inscription (Id_acti, Id_Pers);

create index FKins_CLI_IND
     on inscription (Id_Pers);

create unique index ID_loue_emplacement_IND
     on loue_emplacement (Id_emplacement, Id_Pers);

create index FKlou_CLI_1_IND
     on loue_emplacement (Id_Pers);

create unique index ID_Loue_mat_IND
     on Loue_mat (Id_mat, Id_Pers);

create index FKLou_CLI_IND
     on Loue_mat (Id_Pers);

create unique index ID_MATERIEL_IND
     on MATERIEL (Id_mat);

create unique index ID_NETTOIE_IND
     on NETTOIE (Id_Pers, Heure, Date);

create index FKNET_SEC_IND
     on NETTOIE (Id_secteur);

create unique index ID_participe_IND
     on participe (Id_tournoi, Id_equipe);

create index FKpar_EQU_IND
     on participe (Id_equipe);

create unique index ID_PERSONNE_IND
     on PERSONNE (Id_Pers);

create unique index ID_peut_faire_IND
     on peut_faire (Type_acti, Id_Pers);

create index FKpeu_ANI_IND
     on peut_faire (Id_Pers);

create unique index ID_Prenom_IND
     on Prenom (Id_Pers, Prenom);

create unique index ID_SECTEUR_IND
     on SECTEUR (Id_secteur);

create unique index SID_STAFF_IND
     on STAFF (Id_staff);

create unique index FKPER_STA_IND
     on STAFF (Id_Pers);

create index FKdirige_IND
     on STAFF (Chef_);

create unique index SID_TECHNICIEN_IND
     on TECHNICIEN (Id_tech);

create unique index FKSTA_TEC_IND
     on TECHNICIEN (Id_Pers);

create unique index ID_TOURNOI_IND
     on TOURNOI (Id_tournoi);

create unique index FKde_IND
     on TOURNOI (Id_acti);

create unique index ID_TYPE_ACTI_IND
     on TYPE_ACTI (Type_acti);

