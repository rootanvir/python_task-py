--
-- PostgreSQL database dump
--

\restrict 1FRym3GfetfvJBn89ad9EVGuTieo3Mh2Gho4breaTXPxPXe7HYumv6EkbpR9ts0

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-10-19 01:24:05

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 24576)
-- Name: script; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA script;


ALTER SCHEMA script OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 16404)
-- Name: samsung_phones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.samsung_phones (
    id integer NOT NULL,
    model_name text,
    release_date text,
    display text,
    battery text,
    camera text,
    ram text,
    storage text,
    price text
);


ALTER TABLE public.samsung_phones OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16403)
-- Name: samsung_phones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.samsung_phones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.samsung_phones_id_seq OWNER TO postgres;

--
-- TOC entry 4913 (class 0 OID 0)
-- Dependencies: 220
-- Name: samsung_phones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.samsung_phones_id_seq OWNED BY public.samsung_phones.id;


--
-- TOC entry 4756 (class 2604 OID 16407)
-- Name: samsung_phones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samsung_phones ALTER COLUMN id SET DEFAULT nextval('public.samsung_phones_id_seq'::regclass);


--
-- TOC entry 4907 (class 0 OID 16404)
-- Dependencies: 221
-- Data for Name: samsung_phones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.samsung_phones (id, model_name, release_date, display, battery, camera, ram, storage, price) FROM stdin;
406	Galaxy M17	2025, October 10	Super AMOLED, 90Hz, 1100 nits (HBM)	Li-Po 6000 mAh, non-removable	Triple: 50 MP (wide) + 5 MP (ultrawide) + 2 MP (depth)	4GB RAM	128GB 4GB RAM, 128GB 6GB RAM, 128GB 8GB RAM	About 120 EUR
407	Galaxy F07	2025, October 04	PLS LCD, 90Hz	Li-Po 5000 mAh, non-removable	Dual: 50 MP (wide) + 2 MP (depth)	4GB RAM	64GB 4GB RAM	₹ 7,199
408	Galaxy M07	2025, October 01	PLS LCD, 90Hz	Li-Po 5000 mAh, non-removable	Dual: 50 MP (wide) + 2 MP (depth)	4GB RAM	64GB 4GB RAM	₹ 6,799
409	Galaxy A17 4G	2025, September 18	Super AMOLED, 90Hz	Li-Po 5000 mAh, non-removable	Triple: 50 MP (wide) + 5 MP (ultrawide) + 2 MP (macro)	4GB RAM	128GB 4GB RAM, 256GB 8GB RAM	€ 168.50 / $ 179.97 / £ 149.00
410	Galaxy Tab A11+	2025, September 29	TFT LCD, 90Hz	Li-Po 8000 mAh, non-removable	Single: 13 MP (wide)	N/A	128GB, 256GB	About 250 EUR
411	Galaxy Tab A11	2025, September 12	TFT LCD, 90Hz	Li-Po 7000 mAh, non-removable	Single: 8 MP (wide)	4GB RAM	64GB 4GB RAM, 128GB 8GB RAM	About 200 EUR
412	Galaxy F17	2025, September 11	Super AMOLED, 90Hz, 1100 nits (HBM)	Li-Po 6000 mAh, non-removable	Triple: 50 MP (wide) + 5 MP (ultrawide) + 2 MP (depth)	4GB RAM	128GB 4GB RAM, 128GB 6GB RAM	₹ 13,287
413	Galaxy S25 FE	2025, September 04	Dynamic LTPO AMOLED 2X, 120Hz, HDR10+, 1900 nits (peak)	Li-Ion 4500 mAh, non-removable	Triple: 50 MP (wide) + 12 MP (ultrawide) + 8 MP (telephoto)	8GB RAM	128GB 8GB RAM, 256GB 8GB RAM, 512GB 8GB RAM	€ 595.00 / $ 548.99 / £ 599.00 / ₹ 65,999
414	Galaxy Tab S11 Ultra	2025, September 04	Dynamic AMOLED 2X, 120Hz, HDR10+, 1600 nits (peak)	Li-Po 11200 mAh, non-removable	Dual: 13 MP (wide) + 8 MP (ultrawide)	12GB RAM	128GB 12GB RAM, 256GB 12GB RAM, 512GB 12GB RAM, 1TB 16GB RAM	$ 1,199.00
415	Galaxy Tab S11	2025, September 04	Dynamic AMOLED 2X, 120Hz, HDR10+, 1600 nits (peak)	Li-Po 8400 mAh, non-removable	Single: 13 MP (wide)	12GB RAM	128GB 12GB RAM, 256GB 12GB RAM, 512GB 12GB RAM	$ 899.99
416	Galaxy Tab S10 Lite	2025, August 25	TFT LCD, 90Hz	Li-Po 7500 mAh, non-removable	Single: 13 MP (wide)	6GB RAM	128GB 6GB RAM, 256GB 8GB RAM	About 400 EUR
417	Galaxy A07 4G	2025, August 25	PLS LCD, 90Hz	Li-Po 5000 mAh, non-removable	Dual: 50 MP (wide) + 2 MP (depth)	4GB RAM	64GB 4GB RAM, 128GB 4GB RAM, 128GB 6GB RAM, 256GB 8GB RAM	$ 139.99
418	Galaxy A17	2025, August 06	Super AMOLED, 90Hz, 800 nits (HBM)	Li-Po 5000 mAh, non-removable	Triple: 50 MP (wide) + 5 MP (ultrawide) + 2 MP (macro)	4GB RAM	128GB 4GB RAM, 128GB 6GB RAM, 128GB 8GB RAM, 256GB 4GB RAM, 256GB 8GB RAM	€ 165.00 / $ 211.73 / £ 195.00 / ₹ 16,785
419	Galaxy F36	2025, July 21	Super AMOLED, 120Hz	Li-Po 6000 mAh, non-removable	Triple: 50 MP (wide) + 8 MP (ultrawide) + 2 MP (depth)	6GB RAM	128GB 6GB RAM, 128GB 8GB RAM, 256GB 8GB RAM	₹ 15,989
420	Galaxy Z Fold7	2025, July 09	Foldable Dynamic LTPO AMOLED 2X, 120Hz, HDR10+, 2600 nits (peak)	Li-Po 4600 mAh, non-removable	Triple: 50 MP (wide) + 12 MP (ultrawide) + 10 MP (telephoto)	12GB RAM	256GB 12GB RAM, 512GB 12GB RAM, 1TB 12GB RAM, 1TB 16GB RAM	€ 1,284.90 / $ 1,516.69 / £ 1,598.83 / ₹ 174,999
421	Galaxy Z Flip7	2025, July 09	Foldable Dynamic LTPO AMOLED 2X, 120Hz, HDR10+, 2600 nits (peak)	Li-Po 3700 mAh, non-removable	Dual: 50 MP (wide) + 12 MP (ultrawide)	12GB RAM	256GB 12GB RAM, 512GB 12GB RAM	€ 742.00 / $ 759.00 / £ 932.08 / ₹ 109,999
422	Galaxy Z Flip7 FE	2025, July 09	Foldable Dynamic LTPO AMOLED 2X, 120Hz, HDR10+, 2600 nits (peak)	Li-Po 3900 mAh, non-removable	Dual: 50 MP (wide) + 12 MP (ultrawide)	8GB RAM	128GB 8GB RAM, 256GB 8GB RAM	€ 997.77 / $ 758.99 / £ 816.14 / ₹ 89,999
423	Galaxy Watch8 Classic	2025, July 09	Super AMOLED, 3000 nits (peak)	Li-Ion 425 mAh, non-removable	N/A	2GB RAM	64GB 2GB RAM	€ 313.89
424	Galaxy Watch8	2025, July 09	Super AMOLED, 3000 nits (peak)	Li-Ion 300 mAh, non-removable	N/A	2GB RAM	32GB 2GB RAM	€ 240.87 / $ 359.99
425	Galaxy M36	2025, June 27	Super AMOLED, 120Hz	Li-Po 6000 mAh, non-removable	Triple: 50 MP (wide) + 8 MP (ultrawide) + 2 MP (depth)	6GB RAM	128GB 6GB RAM, 128GB 8GB RAM, 256GB 8GB RAM	₹ 13,999
426	Galaxy S25 Edge	2025, May 13	LTPO AMOLED 2X, 120Hz, 480Hz PWM, HDR10+	Li-Ion 4700 mAh, non-removable	Dual: 50 MP (wide) + 12 MP (ultrawide)	12GB RAM	256GB 12GB RAM, 512GB 12GB RAM	€ 649.90 / $ 529.99 / £ 699.99 / ₹ 101,999
427	Galaxy F56	2025, May 07	Super AMOLED+, 120Hz	Li-Po 6000 mAh, non-removable	Triple: 50 MP (wide) + 8 MP (ultrawide) + 2 MP (depth)	8GB RAM	128GB 8GB RAM, 256GB 8GB RAM	About 270 EUR
428	Galaxy M56	2025, April 17	Super AMOLED+, 120Hz	Li-Po 6000 mAh, non-removable	Triple: 50 MP (wide) + 8 MP (ultrawide) + 2 MP (depth)	8GB RAM	128GB 8GB RAM, 256GB 8GB RAM	₹ 24,999
429	Galaxy XCover7 Pro	2025, April 14	PLS LCD, 120Hz	Li-Ion 4050 mAh, removable	Dual: 50 MP (wide) + 8 MP (ultrawide)	6GB RAM	128GB 6GB RAM	€ 430.00
430	Galaxy Tab Active5 Pro	2025, April 14	TFT LCD, 120Hz	Li-Ion 7600 mAh, removable	Single: 13 MP (wide)	6GB RAM	128GB 6GB RAM, 256GB 8GB RAM	About 900 EUR
\.


--
-- TOC entry 4914 (class 0 OID 0)
-- Dependencies: 220
-- Name: samsung_phones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.samsung_phones_id_seq', 430, true);


--
-- TOC entry 4758 (class 2606 OID 16412)
-- Name: samsung_phones samsung_phones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samsung_phones
    ADD CONSTRAINT samsung_phones_pkey PRIMARY KEY (id);


-- Completed on 2025-10-19 01:24:05

--
-- PostgreSQL database dump complete
--

\unrestrict 1FRym3GfetfvJBn89ad9EVGuTieo3Mh2Gho4breaTXPxPXe7HYumv6EkbpR9ts0

