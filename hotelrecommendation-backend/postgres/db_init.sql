--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id SERIAL NOT NULL,
    username character varying(200),
    password character varying(200),
    role character varying(50),
    PRIMARY KEY (id),
    UNIQUE (username)
);


ALTER TABLE public.users OWNER TO postgres;

INSERT INTO public.users ("username","password","role") VALUES('admin','$2b$10$knGYn2dDWhG1jFK9258YHezBmu53pS6mGl6G7wOy0snwLUtA6OyoS','ADMIN');


CREATE TABLE public.hotels (
    id character varying(50) NOT NULL,
    hotel_owner_id Integer,
    status text,
    city text,
    name text,
    link text,
    img text,
    address text,
    rating double precision,
    price integer,
    FOREIGN KEY (hotel_owner_id) REFERENCES public.users(id),
    UNIQUE(address),
    UNIQUE(id)
);
ALTER TABLE public.hotels OWNER TO postgres;


CREATE TABLE public.feedback (
    id character varying(20) NOT NULL,
    user_id Integer,
    hotel_id character varying(20),
    content text,
    rating double precision,
    FOREIGN KEY (user_id) REFERENCES public.users(id),
    FOREIGN KEY (hotel_id) REFERENCES public.hotels(id)
);
ALTER TABLE public.feedback OWNER TO postgres;

--
-- PostgreSQL database dump complete
--

