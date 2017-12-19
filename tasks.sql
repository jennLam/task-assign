-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.0
-- PostgreSQL version: 9.6
-- Project Site: pgmodeler.com.br
-- Model Author: ---


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: new_database | type: DATABASE --
-- -- DROP DATABASE IF EXISTS new_database;
-- CREATE DATABASE new_database
-- ;
-- -- ddl-end --
-- 

-- object: public."Technician" | type: TABLE --
-- DROP TABLE IF EXISTS public."Technician" CASCADE;
CREATE TABLE public."Technician"(
	id integer NOT NULL,
	name varchar(50) NOT NULL,
	email varchar(100) NOT NULL,
	phone_number integer NOT NULL,
	start_date date NOT NULL,
	"id_TechnicianTask" integer,
	CONSTRAINT "Technician_pk" PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public."Technician" OWNER TO postgres;
-- ddl-end --

-- object: public."Equipment" | type: TABLE --
-- DROP TABLE IF EXISTS public."Equipment" CASCADE;
CREATE TABLE public."Equipment"(
	id integer NOT NULL,
	name varchar(25) NOT NULL,
	ein integer NOT NULL,
	type varchar(25) NOT NULL,
	"id_TaskEquipment" integer,
	"id_Status" integer,
	CONSTRAINT "Equipment_pk" PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public."Equipment" OWNER TO postgres;
-- ddl-end --

-- object: public."Task" | type: TABLE --
-- DROP TABLE IF EXISTS public."Task" CASCADE;
CREATE TABLE public."Task"(
	id integer NOT NULL,
	name varchar(100) NOT NULL,
	details varchar(500),
	"id_TechnicianTask" integer,
	"id_TaskEquipment" integer,
	"id_Status" integer,
	"id_TaskMaterial" integer,
	CONSTRAINT "Task_pk" PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public."Task" OWNER TO postgres;
-- ddl-end --

-- object: public."RawMaterial" | type: TABLE --
-- DROP TABLE IF EXISTS public."RawMaterial" CASCADE;
CREATE TABLE public."RawMaterial"(
	id smallint NOT NULL,
	name varchar(100) NOT NULL,
	details varchar(500),
	"id_TaskMaterial" integer,
	CONSTRAINT "Material_pk" PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public."RawMaterial" OWNER TO postgres;
-- ddl-end --

-- object: public."Status" | type: TABLE --
-- DROP TABLE IF EXISTS public."Status" CASCADE;
CREATE TABLE public."Status"(
	id integer NOT NULL,
	name varchar(50) NOT NULL,
	CONSTRAINT "Status_pk" PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public."Status" OWNER TO postgres;
-- ddl-end --

-- object: public."TaskMaterial" | type: TABLE --
-- DROP TABLE IF EXISTS public."TaskMaterial" CASCADE;
CREATE TABLE public."TaskMaterial"(
	id integer NOT NULL,
	task_id integer NOT NULL,
	material_id integer NOT NULL,
	CONSTRAINT "TaskMaterial_pk" PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public."TaskMaterial" OWNER TO postgres;
-- ddl-end --

-- object: public."TaskEquipment" | type: TABLE --
-- DROP TABLE IF EXISTS public."TaskEquipment" CASCADE;
CREATE TABLE public."TaskEquipment"(
	id integer NOT NULL,
	task_id integer NOT NULL,
	equipment_id integer NOT NULL,
	CONSTRAINT "TaskEquipment_pk" PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public."TaskEquipment" OWNER TO postgres;
-- ddl-end --

-- object: public."TechnicianTask" | type: TABLE --
-- DROP TABLE IF EXISTS public."TechnicianTask" CASCADE;
CREATE TABLE public."TechnicianTask"(
	id integer NOT NULL,
	technician_id integer NOT NULL,
	task_id integer NOT NULL,
	CONSTRAINT "TechnicianTask_pk" PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public."TechnicianTask" OWNER TO postgres;
-- ddl-end --

-- object: "TechnicianTask_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Technician" DROP CONSTRAINT IF EXISTS "TechnicianTask_fk" CASCADE;
ALTER TABLE public."Technician" ADD CONSTRAINT "TechnicianTask_fk" FOREIGN KEY ("id_TechnicianTask")
REFERENCES public."TechnicianTask" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "TechnicianTask_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Task" DROP CONSTRAINT IF EXISTS "TechnicianTask_fk" CASCADE;
ALTER TABLE public."Task" ADD CONSTRAINT "TechnicianTask_fk" FOREIGN KEY ("id_TechnicianTask")
REFERENCES public."TechnicianTask" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "TaskEquipment_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Task" DROP CONSTRAINT IF EXISTS "TaskEquipment_fk" CASCADE;
ALTER TABLE public."Task" ADD CONSTRAINT "TaskEquipment_fk" FOREIGN KEY ("id_TaskEquipment")
REFERENCES public."TaskEquipment" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "TaskEquipment_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Equipment" DROP CONSTRAINT IF EXISTS "TaskEquipment_fk" CASCADE;
ALTER TABLE public."Equipment" ADD CONSTRAINT "TaskEquipment_fk" FOREIGN KEY ("id_TaskEquipment")
REFERENCES public."TaskEquipment" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "Status_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Task" DROP CONSTRAINT IF EXISTS "Status_fk" CASCADE;
ALTER TABLE public."Task" ADD CONSTRAINT "Status_fk" FOREIGN KEY ("id_Status")
REFERENCES public."Status" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "Status_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Equipment" DROP CONSTRAINT IF EXISTS "Status_fk" CASCADE;
ALTER TABLE public."Equipment" ADD CONSTRAINT "Status_fk" FOREIGN KEY ("id_Status")
REFERENCES public."Status" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "TaskMaterial_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Task" DROP CONSTRAINT IF EXISTS "TaskMaterial_fk" CASCADE;
ALTER TABLE public."Task" ADD CONSTRAINT "TaskMaterial_fk" FOREIGN KEY ("id_TaskMaterial")
REFERENCES public."TaskMaterial" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "TaskMaterial_fk" | type: CONSTRAINT --
-- ALTER TABLE public."RawMaterial" DROP CONSTRAINT IF EXISTS "TaskMaterial_fk" CASCADE;
ALTER TABLE public."RawMaterial" ADD CONSTRAINT "TaskMaterial_fk" FOREIGN KEY ("id_TaskMaterial")
REFERENCES public."TaskMaterial" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --


