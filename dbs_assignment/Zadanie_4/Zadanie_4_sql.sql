BEGIN;


CREATE TABLE IF NOT EXISTS public.exemplare
(
    id serial NOT NULL,
    meno character varying(255) COLLATE pg_catalog."default" NOT NULL,
    vlastne boolean NOT NULL,
    pozicane boolean NOT NULL,
    CONSTRAINT exemplare_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.exemplare_expozicie
(
    exemplareid integer NOT NULL,
    expozicieid integer NOT NULL,
    CONSTRAINT exemplare_expozicie_pkey PRIMARY KEY (exemplareid, expozicieid)
);

CREATE TABLE IF NOT EXISTS public.exemplare_kategorie
(
    exemplareid integer NOT NULL,
    kategorieid integer NOT NULL,
    CONSTRAINT exemplare_kategorie_pkey PRIMARY KEY (exemplareid, kategorieid)
);

CREATE TABLE IF NOT EXISTS public.exemplare_zony
(
    exemplareid integer NOT NULL,
    zonyid integer NOT NULL,
    zaciatok timestamp without time zone NOT NULL,
    koniec timestamp without time zone,
    status enum NOT NULL,
    CONSTRAINT exemplare_zony_pkey PRIMARY KEY (exemplareid, zonyid)
);

CREATE TABLE IF NOT EXISTS public.expozicie
(
    id serial NOT NULL,
    meno character varying(255) COLLATE pg_catalog."default" NOT NULL,
    zaciatok timestamp without time zone NOT NULL,
    koniec timestamp without time zone,
    status enum NOT NULL,
    CONSTRAINT expozicie_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.expozicie_zony
(
    expozicieid integer NOT NULL,
    zonyid integer NOT NULL,
    CONSTRAINT expozicie_zony_pkey PRIMARY KEY (expozicieid, zonyid)
);

CREATE TABLE IF NOT EXISTS public.kategorie
(
    id serial NOT NULL,
    meno character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT kategorie_pkey PRIMARY KEY (id),
    CONSTRAINT kategorie_meno_key UNIQUE (meno)
);

CREATE TABLE IF NOT EXISTS public.kontroly
(
    id serial NOT NULL,
    zaciatok timestamp without time zone NOT NULL,
    koniec timestamp without time zone,
    stav enum NOT NULL,
    exemplareid integer NOT NULL,
    CONSTRAINT kontroly_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.stav
(
    id serial NOT NULL,
    zaciatok timestamp without time zone NOT NULL,
    koniec timestamp without time zone,
    stav enum NOT NULL,
    status enum NOT NULL,
    exemplareid integer NOT NULL,
    CONSTRAINT stav_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.vlastnik
(
    id serial NOT NULL,
    meno character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT vlastnik_pkey PRIMARY KEY (id),
    CONSTRAINT vlastnik_meno_key UNIQUE (meno)
);

CREATE TABLE IF NOT EXISTS public.vlastnik_exemplare
(
    exemplareid integer NOT NULL,
    vlastnikid integer NOT NULL,
    zaciatok timestamp without time zone NOT NULL,
    koniec timestamp without time zone,
    CONSTRAINT vlastnik_exemplare_pkey PRIMARY KEY (exemplareid, vlastnikid)
);

CREATE TABLE IF NOT EXISTS public.zony
(
    id serial NOT NULL,
    meno character varying(255) COLLATE pg_catalog."default" NOT NULL,
    rozloha integer NOT NULL,
    CONSTRAINT zony_pkey PRIMARY KEY (id),
    CONSTRAINT zony_meno_key UNIQUE (meno)
);

ALTER TABLE IF EXISTS public.exemplare_expozicie
    ADD CONSTRAINT fkexemplare_604629 FOREIGN KEY (expozicieid)
    REFERENCES public.expozicie (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.exemplare_expozicie
    ADD CONSTRAINT fkexemplare_693723 FOREIGN KEY (exemplareid)
    REFERENCES public.exemplare (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.exemplare_kategorie
    ADD CONSTRAINT fkexemplare_226804 FOREIGN KEY (kategorieid)
    REFERENCES public.kategorie (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.exemplare_kategorie
    ADD CONSTRAINT fkexemplare_48913 FOREIGN KEY (exemplareid)
    REFERENCES public.exemplare (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.exemplare_zony
    ADD CONSTRAINT fkexemplare_133904 FOREIGN KEY (zonyid)
    REFERENCES public.zony (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.exemplare_zony
    ADD CONSTRAINT fkexemplare_582027 FOREIGN KEY (exemplareid)
    REFERENCES public.exemplare (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.expozicie_zony
    ADD CONSTRAINT fkexpozicie_425347 FOREIGN KEY (zonyid)
    REFERENCES public.zony (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.expozicie_zony
    ADD CONSTRAINT fkexpozicie_799766 FOREIGN KEY (expozicieid)
    REFERENCES public.expozicie (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.kontroly
    ADD CONSTRAINT fkkontroly462500 FOREIGN KEY (exemplareid)
    REFERENCES public.exemplare (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.stav
    ADD CONSTRAINT fkstav569385 FOREIGN KEY (exemplareid)
    REFERENCES public.exemplare (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.vlastnik_exemplare
    ADD CONSTRAINT fkvlastnik_e151438 FOREIGN KEY (vlastnikid)
    REFERENCES public.vlastnik (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.vlastnik_exemplare
    ADD CONSTRAINT fkvlastnik_e174466 FOREIGN KEY (exemplareid)
    REFERENCES public.exemplare (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;