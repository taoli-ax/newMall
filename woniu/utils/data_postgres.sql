--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;


--insert into public.tb_brand (id, name, logo, first_letter) values
--(1,'Apple','group1/M00/00/02/CtM3BVrOMI-AVPWrAAAPN5YrVxw2187795','A'),
--(2,'华为（HUAWEI）','group1/M00/00/02/CtM3BVrRbvmAJ0cWAAAefuA2Xqo3496149','H');



insert into public.tb_channel_group (id, name) values
(1,'手机数码'),
(2,'电脑家电'),
(3,'家居家装'),
(4,'男女童装'),
(5,'女鞋箱包'),
(6,'手机数码'),
(7,'运动户外'),
(8,'房产汽车')
(9,'食品生鲜'),
(10,'图书音像'),
(11,'旅游生活');



