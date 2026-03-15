--
-- PostgreSQL database dump
--

\restrict rxSmI8O8r4q8ujTElvx2pqABCL56ATwxV9Gr8bG20OAI1ITTdOSS0C0Bi2QkfCu

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.claims_patient DROP CONSTRAINT IF EXISTS claims_patient_ipm_id_6942c307_fk_claims_ipm_id;
ALTER TABLE IF EXISTS ONLY public.claims_patient DROP CONSTRAINT IF EXISTS claims_patient_coverage_plan_id_6d4b902e_fk_claims_co;
ALTER TABLE IF EXISTS ONLY public.claims_notificationlog DROP CONSTRAINT IF EXISTS claims_notificationlog_claim_id_b6e75016_fk_claims_claim_id;
ALTER TABLE IF EXISTS ONLY public.claims_ipmpaymentoption DROP CONSTRAINT IF EXISTS claims_ipmpaymentoption_ipm_id_cb509215_fk_claims_ipm_id;
ALTER TABLE IF EXISTS ONLY public.claims_ipmpaymentoption DROP CONSTRAINT IF EXISTS claims_ipmpaymentoption_deleted_by_id_0ec82b0e_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.claims_ipmpaymentoption DROP CONSTRAINT IF EXISTS claims_ipmpaymentopt_payment_method_id_7fbb0924_fk_claims_pa;
ALTER TABLE IF EXISTS ONLY public.claims_ipm DROP CONSTRAINT IF EXISTS claims_ipm_deleted_by_id_8022a2c0_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.claims_hospital DROP CONSTRAINT IF EXISTS claims_hospital_deleted_by_id_43fdc6f4_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.claims_establishmentpaymentoption DROP CONSTRAINT IF EXISTS claims_establishment_payment_method_id_0587b8c6_fk_claims_pa;
ALTER TABLE IF EXISTS ONLY public.claims_establishmentpaymentoption DROP CONSTRAINT IF EXISTS claims_establishment_hospital_id_ca790a41_fk_claims_ho;
ALTER TABLE IF EXISTS ONLY public.claims_establishmentpaymentoption DROP CONSTRAINT IF EXISTS claims_establishment_deleted_by_id_d16cf8e7_fk_auth_user;
ALTER TABLE IF EXISTS ONLY public.claims_coveragerule DROP CONSTRAINT IF EXISTS claims_coveragerule_coverage_plan_id_289a27db_fk_claims_co;
ALTER TABLE IF EXISTS ONLY public.claims_coveragerule DROP CONSTRAINT IF EXISTS claims_coveragerule_category_id_3ce30a5e_fk_claims_category_id;
ALTER TABLE IF EXISTS ONLY public.claims_coverageplan DROP CONSTRAINT IF EXISTS claims_coverageplan_ipm_id_33660a0a_fk_claims_ipm_id;
ALTER TABLE IF EXISTS ONLY public.claims_claimdocument DROP CONSTRAINT IF EXISTS claims_claimdocument_claim_id_c1c69bf4_fk_claims_claim_id;
ALTER TABLE IF EXISTS ONLY public.claims_claimauditlog DROP CONSTRAINT IF EXISTS claims_claimauditlog_claim_id_1275ed2d_fk_claims_claim_id;
ALTER TABLE IF EXISTS ONLY public.claims_claimauditlog DROP CONSTRAINT IF EXISTS claims_claimauditlog_actor_id_1101d5f7_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.claims_claim DROP CONSTRAINT IF EXISTS claims_claim_provider_id_45721be3_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.claims_claim DROP CONSTRAINT IF EXISTS claims_claim_patient_id_c2aa2b02_fk_claims_patient_id;
ALTER TABLE IF EXISTS ONLY public.claims_claim DROP CONSTRAINT IF EXISTS claims_claim_deleted_by_id_162ba72d_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.claims_claim DROP CONSTRAINT IF EXISTS claims_claim_category_id_872bdf1a_fk_claims_category_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.accounts_staffprofile DROP CONSTRAINT IF EXISTS accounts_staffprofile_user_id_1ed1af60_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.accounts_staffprofile DROP CONSTRAINT IF EXISTS accounts_staffprofile_ipm_id_ba365394_fk_claims_ipm_id;
ALTER TABLE IF EXISTS ONLY public.accounts_staffprofile DROP CONSTRAINT IF EXISTS accounts_staffprofile_deleted_by_id_87c58fb0_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.accounts_staffprofile DROP CONSTRAINT IF EXISTS accounts_staffprofil_hospital_id_465f1649_fk_claims_ho;
DROP INDEX IF EXISTS public.unique_ipm_payment_option;
DROP INDEX IF EXISTS public.unique_ipm_name_not_deleted;
DROP INDEX IF EXISTS public.unique_ipm_code_not_deleted;
DROP INDEX IF EXISTS public.unique_hospital_name_not_deleted;
DROP INDEX IF EXISTS public.unique_hospital_code_not_deleted;
DROP INDEX IF EXISTS public.unique_establishment_payment_option;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.claims_paymentmethod_name_b977624f_like;
DROP INDEX IF EXISTS public.claims_paymentmethod_code_203ec9c4_like;
DROP INDEX IF EXISTS public.claims_patient_ipm_id_6942c307;
DROP INDEX IF EXISTS public.claims_patient_coverage_plan_id_6d4b902e;
DROP INDEX IF EXISTS public.claims_notificationlog_claim_id_b6e75016;
DROP INDEX IF EXISTS public.claims_notificationchannelconfig_channel_a957fde6_like;
DROP INDEX IF EXISTS public.claims_ipmpaymentoption_payment_method_id_7fbb0924;
DROP INDEX IF EXISTS public.claims_ipmpaymentoption_ipm_id_cb509215;
DROP INDEX IF EXISTS public.claims_ipmpaymentoption_deleted_by_id_0ec82b0e;
DROP INDEX IF EXISTS public.claims_ipm_deleted_by_id_8022a2c0;
DROP INDEX IF EXISTS public.claims_hospital_deleted_by_id_43fdc6f4;
DROP INDEX IF EXISTS public.claims_establishmentpaymentoption_payment_method_id_0587b8c6;
DROP INDEX IF EXISTS public.claims_establishmentpaymentoption_hospital_id_ca790a41;
DROP INDEX IF EXISTS public.claims_establishmentpaymentoption_deleted_by_id_d16cf8e7;
DROP INDEX IF EXISTS public.claims_coveragerule_coverage_plan_id_289a27db;
DROP INDEX IF EXISTS public.claims_coveragerule_category_id_3ce30a5e;
DROP INDEX IF EXISTS public.claims_coverageplan_ipm_id_33660a0a;
DROP INDEX IF EXISTS public.claims_claimdocument_claim_id_c1c69bf4;
DROP INDEX IF EXISTS public.claims_claimauditlog_claim_id_1275ed2d;
DROP INDEX IF EXISTS public.claims_claimauditlog_actor_id_1101d5f7;
DROP INDEX IF EXISTS public.claims_claim_provider_id_45721be3;
DROP INDEX IF EXISTS public.claims_claim_patient_token_3e5d3564_like;
DROP INDEX IF EXISTS public.claims_claim_patient_id_c2aa2b02;
DROP INDEX IF EXISTS public.claims_claim_deleted_by_id_162ba72d;
DROP INDEX IF EXISTS public.claims_claim_category_id_872bdf1a;
DROP INDEX IF EXISTS public.claims_category_name_42e04624_like;
DROP INDEX IF EXISTS public.auth_user_username_6821ab7c_like;
DROP INDEX IF EXISTS public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX IF EXISTS public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX IF EXISTS public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX IF EXISTS public.auth_user_groups_group_id_97559544;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
DROP INDEX IF EXISTS public.accounts_staffprofile_ipm_id_ba365394;
DROP INDEX IF EXISTS public.accounts_staffprofile_hospital_id_465f1649;
DROP INDEX IF EXISTS public.accounts_staffprofile_deleted_by_id_87c58fb0;
ALTER TABLE IF EXISTS ONLY public.claims_coverageplan DROP CONSTRAINT IF EXISTS unique_plan_per_ipm;
ALTER TABLE IF EXISTS ONLY public.claims_patient DROP CONSTRAINT IF EXISTS unique_patient_per_ipm;
ALTER TABLE IF EXISTS ONLY public.claims_coveragerule DROP CONSTRAINT IF EXISTS unique_coverage_per_plan_category;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_paymentmethod DROP CONSTRAINT IF EXISTS claims_paymentmethod_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_paymentmethod DROP CONSTRAINT IF EXISTS claims_paymentmethod_name_key;
ALTER TABLE IF EXISTS ONLY public.claims_paymentmethod DROP CONSTRAINT IF EXISTS claims_paymentmethod_code_key;
ALTER TABLE IF EXISTS ONLY public.claims_patient DROP CONSTRAINT IF EXISTS claims_patient_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_notificationlog DROP CONSTRAINT IF EXISTS claims_notificationlog_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_notificationchannelconfig DROP CONSTRAINT IF EXISTS claims_notificationchannelconfig_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_notificationchannelconfig DROP CONSTRAINT IF EXISTS claims_notificationchannelconfig_channel_key;
ALTER TABLE IF EXISTS ONLY public.claims_ipmpaymentoption DROP CONSTRAINT IF EXISTS claims_ipmpaymentoption_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_ipm DROP CONSTRAINT IF EXISTS claims_ipm_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_hospital DROP CONSTRAINT IF EXISTS claims_hospital_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_establishmentpaymentoption DROP CONSTRAINT IF EXISTS claims_establishmentpaymentoption_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_coveragerule DROP CONSTRAINT IF EXISTS claims_coveragerule_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_coverageplan DROP CONSTRAINT IF EXISTS claims_coverageplan_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_claimdocument DROP CONSTRAINT IF EXISTS claims_claimdocument_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_claimauditlog DROP CONSTRAINT IF EXISTS claims_claimauditlog_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_claim DROP CONSTRAINT IF EXISTS claims_claim_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_claim DROP CONSTRAINT IF EXISTS claims_claim_patient_token_key;
ALTER TABLE IF EXISTS ONLY public.claims_category DROP CONSTRAINT IF EXISTS claims_category_pkey;
ALTER TABLE IF EXISTS ONLY public.claims_category DROP CONSTRAINT IF EXISTS claims_category_name_key;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_username_key;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.accounts_staffprofile DROP CONSTRAINT IF EXISTS accounts_staffprofile_user_id_key;
ALTER TABLE IF EXISTS ONLY public.accounts_staffprofile DROP CONSTRAINT IF EXISTS accounts_staffprofile_pkey;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.claims_paymentmethod;
DROP TABLE IF EXISTS public.claims_patient;
DROP TABLE IF EXISTS public.claims_notificationlog;
DROP TABLE IF EXISTS public.claims_notificationchannelconfig;
DROP TABLE IF EXISTS public.claims_ipmpaymentoption;
DROP TABLE IF EXISTS public.claims_ipm;
DROP TABLE IF EXISTS public.claims_hospital;
DROP TABLE IF EXISTS public.claims_establishmentpaymentoption;
DROP TABLE IF EXISTS public.claims_coveragerule;
DROP TABLE IF EXISTS public.claims_coverageplan;
DROP TABLE IF EXISTS public.claims_claimdocument;
DROP TABLE IF EXISTS public.claims_claimauditlog;
DROP TABLE IF EXISTS public.claims_claim;
DROP TABLE IF EXISTS public.claims_category;
DROP TABLE IF EXISTS public.auth_user_user_permissions;
DROP TABLE IF EXISTS public.auth_user_groups;
DROP TABLE IF EXISTS public.auth_user;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.accounts_staffprofile;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts_staffprofile; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts_staffprofile (
    id bigint NOT NULL,
    role character varying(20) NOT NULL,
    ipm_name character varying(120) NOT NULL,
    user_id integer NOT NULL,
    deleted_at timestamp with time zone,
    is_deleted boolean NOT NULL,
    deleted_by_id integer,
    organisation_name character varying(150) NOT NULL,
    hospital_id bigint,
    ipm_id bigint
);


--
-- Name: accounts_staffprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.accounts_staffprofile ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_staffprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_category (
    id bigint NOT NULL,
    name character varying(120) NOT NULL,
    is_pharmacy boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: claims_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_category ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_claim; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_claim (
    id bigint NOT NULL,
    status character varying(25) NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    medicine_names text NOT NULL,
    submitted_at timestamp with time zone,
    locked_at timestamp with time zone,
    snapshot_json jsonb NOT NULL,
    patient_token character varying(128),
    token_expires_at timestamp with time zone,
    token_used_at timestamp with time zone,
    block_reason character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    category_id bigint NOT NULL,
    provider_id integer NOT NULL,
    patient_id bigint NOT NULL,
    care_date date,
    invoice_number character varying(80) NOT NULL,
    deleted_at timestamp with time zone,
    is_deleted boolean NOT NULL,
    deleted_by_id integer,
    dispute_reason text NOT NULL
);


--
-- Name: claims_claim_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_claim ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_claim_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_claimauditlog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_claimauditlog (
    id bigint NOT NULL,
    event character varying(80) NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    actor_id integer,
    claim_id bigint NOT NULL
);


--
-- Name: claims_claimauditlog_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_claimauditlog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_claimauditlog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_claimdocument; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_claimdocument (
    id bigint NOT NULL,
    file character varying(100) NOT NULL,
    original_name character varying(255) NOT NULL,
    uploaded_at timestamp with time zone NOT NULL,
    claim_id bigint NOT NULL,
    document_type character varying(25) NOT NULL
);


--
-- Name: claims_claimdocument_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_claimdocument ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_claimdocument_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_coverageplan; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_coverageplan (
    id bigint NOT NULL,
    name character varying(150) NOT NULL,
    annual_ceiling numeric(12,2),
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    ipm_id bigint NOT NULL
);


--
-- Name: claims_coverageplan_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_coverageplan ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_coverageplan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_coveragerule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_coveragerule (
    id bigint NOT NULL,
    coverage_percent numeric(5,2) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    category_id bigint NOT NULL,
    coverage_plan_id bigint
);


--
-- Name: claims_coveragerule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_coveragerule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_coveragerule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_establishmentpaymentoption; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_establishmentpaymentoption (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    phone character varying(30) NOT NULL,
    iban character varying(40) NOT NULL,
    bank_name character varying(120) NOT NULL,
    payee_name character varying(120) NOT NULL,
    reference_notes character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    deleted_by_id integer,
    hospital_id bigint NOT NULL,
    payment_method_id bigint NOT NULL
);


--
-- Name: claims_establishmentpaymentoption_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_establishmentpaymentoption ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_establishmentpaymentoption_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_hospital; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_hospital (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    name character varying(120) NOT NULL,
    code character varying(30),
    address character varying(255) NOT NULL,
    city character varying(80) NOT NULL,
    phone character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    deleted_by_id integer,
    establishment_type character varying(20) NOT NULL
);


--
-- Name: claims_hospital_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_hospital ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_hospital_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_ipm; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_ipm (
    id bigint NOT NULL,
    name character varying(120) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    address character varying(255) NOT NULL,
    city character varying(80) NOT NULL,
    code character varying(30),
    email character varying(254) NOT NULL,
    phone character varying(30) NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    deleted_at timestamp with time zone,
    is_deleted boolean NOT NULL,
    deleted_by_id integer
);


--
-- Name: claims_ipm_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_ipm ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_ipm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_ipmpaymentoption; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_ipmpaymentoption (
    id bigint NOT NULL,
    phone character varying(30) NOT NULL,
    iban character varying(40) NOT NULL,
    bank_name character varying(120) NOT NULL,
    payee_name character varying(120) NOT NULL,
    reference_notes character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    ipm_id bigint NOT NULL,
    payment_method_id bigint NOT NULL,
    deleted_at timestamp with time zone,
    is_deleted boolean NOT NULL,
    deleted_by_id integer
);


--
-- Name: claims_ipmpaymentoption_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_ipmpaymentoption ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_ipmpaymentoption_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_notificationchannelconfig; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_notificationchannelconfig (
    id bigint NOT NULL,
    channel character varying(20) NOT NULL,
    is_active boolean NOT NULL,
    config jsonb NOT NULL,
    last_tested_at timestamp with time zone,
    last_test_error text NOT NULL
);


--
-- Name: claims_notificationchannelconfig_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_notificationchannelconfig ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_notificationchannelconfig_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_notificationlog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_notificationlog (
    id bigint NOT NULL,
    channel character varying(20) NOT NULL,
    target character varying(255) NOT NULL,
    sent_at timestamp with time zone NOT NULL,
    status character varying(20) NOT NULL,
    claim_id bigint NOT NULL,
    error_message text NOT NULL
);


--
-- Name: claims_notificationlog_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_notificationlog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_notificationlog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_patient; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_patient (
    id bigint NOT NULL,
    full_name character varying(150) NOT NULL,
    phone character varying(30) NOT NULL,
    member_number character varying(80) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    ipm_id bigint NOT NULL,
    beneficiary_type character varying(20) NOT NULL,
    coverage_plan_id bigint,
    address character varying(255) NOT NULL,
    city character varying(80) NOT NULL,
    date_of_birth date,
    email character varying(254) NOT NULL,
    gender character varying(10) NOT NULL,
    id_number character varying(50) NOT NULL,
    notes text NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id_document character varying(100)
);


--
-- Name: claims_patient_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_patient ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_patient_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: claims_paymentmethod; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims_paymentmethod (
    id bigint NOT NULL,
    name character varying(80) NOT NULL,
    code character varying(30),
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    method_type character varying(20) NOT NULL
);


--
-- Name: claims_paymentmethod_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.claims_paymentmethod ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.claims_paymentmethod_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Data for Name: accounts_staffprofile; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_staffprofile (id, role, ipm_name, user_id, deleted_at, is_deleted, deleted_by_id, organisation_name, hospital_id, ipm_id) FROM stdin;
1	SYSTEM_ADMIN		1	\N	f	\N		\N	\N
4	SYSTEM_ADMIN		4	\N	f	\N		\N	\N
6	DOCTOR		6	\N	f	\N		1	\N
3	IPM_ADMIN	IPM SANTE PLUS	3	\N	f	\N		\N	1
7	PHARMACY		7	\N	f	\N		3	\N
2	DOCTOR		2	\N	f	\N		1	1
5	IPM_ADMIN	ABOU	5	\N	f	\N		\N	2
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	3	add_permission
6	Can change permission	3	change_permission
7	Can delete permission	3	delete_permission
8	Can view permission	3	view_permission
9	Can add group	2	add_group
10	Can change group	2	change_group
11	Can delete group	2	delete_group
12	Can view group	2	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add staff profile	7	add_staffprofile
26	Can change staff profile	7	change_staffprofile
27	Can delete staff profile	7	delete_staffprofile
28	Can view staff profile	7	view_staffprofile
29	Can add category	8	add_category
30	Can change category	8	change_category
31	Can delete category	8	delete_category
32	Can view category	8	view_category
33	Can add ipm	13	add_ipm
34	Can change ipm	13	change_ipm
35	Can delete ipm	13	delete_ipm
36	Can view ipm	13	view_ipm
37	Can add claim	9	add_claim
38	Can change claim	9	change_claim
39	Can delete claim	9	delete_claim
40	Can view claim	9	view_claim
41	Can add claim audit log	10	add_claimauditlog
42	Can change claim audit log	10	change_claimauditlog
43	Can delete claim audit log	10	delete_claimauditlog
44	Can view claim audit log	10	view_claimauditlog
45	Can add claim document	11	add_claimdocument
46	Can change claim document	11	change_claimdocument
47	Can delete claim document	11	delete_claimdocument
48	Can view claim document	11	view_claimdocument
49	Can add notification log	14	add_notificationlog
50	Can change notification log	14	change_notificationlog
51	Can delete notification log	14	delete_notificationlog
52	Can view notification log	14	view_notificationlog
53	Can add patient	15	add_patient
54	Can change patient	15	change_patient
55	Can delete patient	15	delete_patient
56	Can view patient	15	view_patient
57	Can add coverage rule	12	add_coveragerule
58	Can change coverage rule	12	change_coveragerule
59	Can delete coverage rule	12	delete_coveragerule
60	Can view coverage rule	12	view_coveragerule
61	Can add coverage plan	16	add_coverageplan
62	Can change coverage plan	16	change_coverageplan
63	Can delete coverage plan	16	delete_coverageplan
64	Can view coverage plan	16	view_coverageplan
65	Can add Moyen de paiement	17	add_paymentmethod
66	Can change Moyen de paiement	17	change_paymentmethod
67	Can delete Moyen de paiement	17	delete_paymentmethod
68	Can view Moyen de paiement	17	view_paymentmethod
69	Can add Moyen de paiement IPM	18	add_ipmpaymentoption
70	Can change Moyen de paiement IPM	18	change_ipmpaymentoption
71	Can delete Moyen de paiement IPM	18	delete_ipmpaymentoption
72	Can view Moyen de paiement IPM	18	view_ipmpaymentoption
73	Can add Hôpital / Pharmacie	19	add_hospital
74	Can change Hôpital / Pharmacie	19	change_hospital
75	Can delete Hôpital / Pharmacie	19	delete_hospital
76	Can view Hôpital / Pharmacie	19	view_hospital
77	Can add Configuration notification	20	add_notificationchannelconfig
78	Can change Configuration notification	20	change_notificationchannelconfig
79	Can delete Configuration notification	20	delete_notificationchannelconfig
80	Can view Configuration notification	20	view_notificationchannelconfig
81	Can add Moyen de paiement établissement	21	add_establishmentpaymentoption
82	Can change Moyen de paiement établissement	21	change_establishmentpaymentoption
83	Can delete Moyen de paiement établissement	21	delete_establishmentpaymentoption
84	Can view Moyen de paiement établissement	21	view_establishmentpaymentoption
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
3	pbkdf2_sha256$1200000$5BhEhKMwk2pOZSOY6LTePo$xnZK6abDfg2EWmBZhns4gel1OfPNoZzKKoUeUYemwoI=	\N	f	ipmadmin1			ipm1@remedy.local	t	t	2026-02-15 20:13:59.720521+00
1	pbkdf2_sha256$1200000$BpF7GqEbl6eE4ohZa0GMv3$eB895ZLw58FBktndaA8S3AccNgsPP5QrrLvjeRQ1oAU=	2026-02-20 20:49:05.131591+00	t	superadmin			superadmin@remedy.local	t	t	2026-02-15 20:13:58.902136+00
4	pbkdf2_sha256$1200000$1ON7WXUilkyTScWIBquRM1$7DKy9ZBbfQKuV+e0d4aAQ7pH1RA/Rv0dnkkNVSU6XT8=	2026-03-04 04:30:05.935501+00	t	admin			admin@remedy.sn	t	t	2026-02-19 23:57:48.592212+00
6	pbkdf2_sha256$1200000$LmhijLysdZ62YcNF75ut5J$bUDI3CPx4qunM22tQwZpaThym5AjO7K1CR1rThhy5zs=	2026-03-04 05:45:04.034494+00	f	aminata			aminata@clinique-espoir.sn	f	t	2026-02-19 23:57:49.389878+00
5	pbkdf2_sha256$1200000$TbVaekwt6KXhvkmC51k5U1$ldEqxs0XYuqNedYrvpl26OuOuhBfSa9dbKACDZLMxmA=	2026-03-04 05:53:37.665304+00	f	fatou			fatou@santeplus.sn	f	t	2026-02-19 23:57:48.97855+00
2	pbkdf2_sha256$1200000$4G7w3OzIhH2j8DRGIuwOAa$diozuj7kNH7AVs81m/gr04hGxYdKh00HX3N2qVNtU5M=	2026-02-15 20:15:38.84456+00	f	doctor1			doctor1@remedy.local	f	t	2026-02-15 20:13:59.284048+00
7	pbkdf2_sha256$1200000$wBTtJoItpzVj0ZRy0zMWNb$rOPcJx1NVR0b+LS+JjsghuPZXIuu9CY4QZX3H59ynbA=	2026-02-25 04:26:54.888562+00	f	pharma			pharma@centrale.sn	f	t	2026-02-19 23:57:49.743719+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: claims_category; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_category (id, name, is_pharmacy, is_active, created_at) FROM stdin;
1	Consultation	f	t	2026-02-15 20:14:00.17959+00
2	Pharmacie	t	t	2026-02-15 20:14:00.187329+00
3	Consultation generale	f	t	2026-02-19 23:59:38.293825+00
4	Consultation specialisee	f	t	2026-02-19 23:59:38.297493+00
5	Hospitalisation	f	t	2026-02-19 23:59:38.300093+00
6	Urgences	f	t	2026-02-19 23:59:38.302156+00
7	Chirurgie	f	t	2026-02-19 23:59:38.304413+00
8	Anesthesie	f	t	2026-02-19 23:59:38.306478+00
9	Imagerie	f	t	2026-02-19 23:59:38.308767+00
10	Radiologie	f	t	2026-02-19 23:59:38.310596+00
11	Echographie	f	t	2026-02-19 23:59:38.313153+00
12	Scanner	f	t	2026-02-19 23:59:38.315436+00
13	IRM	f	t	2026-02-19 23:59:38.318322+00
14	Laboratoire	f	t	2026-02-19 23:59:38.320708+00
15	Biologie	f	t	2026-02-19 23:59:38.322793+00
16	Analyse sanguine	f	t	2026-02-19 23:59:38.324622+00
17	Soins dentaires	f	t	2026-02-19 23:59:38.328117+00
18	Ophtalmologie	f	t	2026-02-19 23:59:38.329827+00
19	Maternite	f	t	2026-02-19 23:59:38.332095+00
20	Pediatrie	f	t	2026-02-19 23:59:38.334626+00
21	Kinesitherapie	f	t	2026-02-19 23:59:38.337888+00
22	Vaccination	f	t	2026-02-19 23:59:38.339818+00
23	Medicaments generiques	t	t	2026-02-19 23:59:38.341465+00
24	Medicaments de marque	t	t	2026-02-19 23:59:38.342964+00
25	Dispositifs medicaux	t	t	2026-02-19 23:59:38.345019+00
26	Consommables medicaux	t	t	2026-02-19 23:59:38.346467+00
\.


--
-- Data for Name: claims_claim; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_claim (id, status, total_amount, medicine_names, submitted_at, locked_at, snapshot_json, patient_token, token_expires_at, token_used_at, block_reason, created_at, updated_at, category_id, provider_id, patient_id, care_date, invoice_number, deleted_at, is_deleted, deleted_by_id, dispute_reason) FROM stdin;
11	DRAFT	35000.00		\N	\N	{}	\N	\N	\N		2026-03-04 05:48:44.190185+00	2026-03-04 05:48:44.190195+00	1	6	5	2026-03-04	FAC-TEST-AWA-002	\N	f	\N	
6	READY_FOR_PAYMENT	260000.00	test	2026-02-20 19:07:59.076581+00	2026-02-20 19:07:59.087778+00	{"ipm": "FatouIPM", "formule": "Formule standard", "patient": "Abbbb xdfxdfx", "category": "Biologie", "claim_id": 6, "ipm_share": "208000.00", "locked_at": "2026-02-20T19:07:59.087736+00:00", "total_amount": "260000.00", "patient_share": "52000.00", "medicine_names": "test", "coverage_percent": "80.00"}	eeca2cbf1e5c6f4a9d09915ecab355f30d07438d4c08550b05f403dbb4176589	2026-02-23 19:07:59.087805+00	2026-02-20 19:09:30.663425+00		2026-02-20 19:07:54.786807+00	2026-02-20 19:09:30.666956+00	15	6	3	2026-02-20	23	\N	f	\N	
1	READY_FOR_PAYMENT	25000.00	Paracetamol 1g, Vitamine C	2026-02-15 20:16:20.439236+00	2026-02-15 20:17:04.483355+00	{"ipm": "IPM SANTE PLUS", "patient": "Moussa Diop", "category": "Pharmacie", "claim_id": 1, "ipm_share": "15000.00", "locked_at": "2026-02-15T20:17:04.483327+00:00", "total_amount": "25000.00", "patient_share": "10000.00", "medicine_names": "Paracetamol 1g, Vitamine C", "coverage_percent": "60.00"}	3cbc448604f0466b0d9102ca5469f21f8c60f30f350af3d8e624e46dc97923ed	2026-02-18 20:17:04.483368+00	2026-02-15 20:17:21.794517+00		2026-02-15 20:16:09.237704+00	2026-02-15 20:17:21.796698+00	2	2	1	\N		\N	f	\N	
7	DRAFT	25000.00		\N	\N	{}	\N	\N	\N		2026-02-25 04:43:15.256904+00	2026-02-25 04:43:15.256915+00	1	6	3	2025-02-25		\N	f	\N	
8	DRAFT	150000.00		\N	\N	{}	\N	\N	\N		2026-02-25 23:23:43.866548+00	2026-02-25 23:23:43.866557+00	6	6	2	2026-02-18	128879	\N	f	\N	
2	BLOCKED	12000.00		2026-02-15 20:17:43.337026+00	2026-02-15 20:17:43.343472+00	{"ipm": "IPM SANTE PLUS", "patient": "Moussa Diop", "category": "Consultation", "claim_id": 2, "ipm_share": "7000.00", "locked_at": "2026-02-15T20:17:43.343449+00:00", "total_amount": "10000", "patient_share": "3000.00", "medicine_names": "", "coverage_percent": "70.00"}	ef21d9baff37af4126440b2656fd0e49e8a65a71ed14570770ca8dcc0ca361a5	2026-02-18 20:17:43.343486+00	2026-02-15 20:17:43.349096+00	Fraud suspicion: snapshot mismatch	2026-02-15 20:17:43.334522+00	2026-02-15 20:17:43.349188+00	1	2	1	\N		\N	f	\N	
3	SUBMITTED	280000.00		2026-02-20 01:54:47+00	\N	{}	\N	\N	\N		2026-02-20 01:54:23.342093+00	2026-02-20 02:10:53.15342+00	1	6	3	2026-02-20	12	2026-02-20 02:11:08.3438+00	t	\N	
9	READY_FOR_PAYMENT	35000.00		\N	2026-03-04 04:23:03+00	{"ipm": "IPM SANTE PLUS", "formule": "Formule Standard", "patient": "Moussa Diop", "category": "Consultation", "claim_id": 9, "ipm_share": "24500.00", "locked_at": "2026-03-04T04:23:03.095736+00:00", "total_amount": "35000.00", "patient_share": "10500.00", "medicine_names": "", "coverage_percent": "70.00"}	6e60306370a3e270394ffb7ff01bca61f7e8c24e926506f3d738fa806a115376	2026-03-07 04:23:03+00	\N		2026-03-04 04:21:31.717295+00	2026-03-04 04:23:59.822583+00	1	4	1	2026-03-04	FAC-DEMO-2026-001	\N	f	\N	
4	BLOCKED	280000.00		2026-02-20 02:12:03.916046+00	2026-02-20 02:12:03.92227+00	{"ipm": "FatouIPM", "formule": "Formule standard", "patient": "Abbbb xdfxdfx", "category": "Consultation", "claim_id": 4, "ipm_share": "224000.00", "locked_at": "2026-02-20T02:12:03.922244+00:00", "total_amount": "280000.00", "patient_share": "56000.00", "medicine_names": "", "coverage_percent": "80.00"}	0b182a569ca8de52a317146ad5b1396b9c04937303da20cb278d86245e8610ee	2026-02-23 02:12:03.922284+00	2026-02-20 03:06:35.600856+00	Je pense que y’a des erreurs	2026-02-20 02:11:53.725702+00	2026-02-20 03:06:35.611196+00	1	6	3	2026-02-20	12	\N	f	\N	Je pense que y’a des erreurs
5	DRAFT	260000.00	test	\N	\N	{}	\N	\N	\N		2026-02-20 19:07:09.360677+00	2026-02-20 19:07:09.360684+00	15	6	3	2026-02-20	23	\N	f	\N	
10	READY_FOR_PAYMENT	45000.00		\N	2026-03-04 04:30:43.520927+00	{"ipm": "IPM Horizon Santé", "formule": "Formule standard", "patient": "Seynabou Fall", "category": "Consultation", "claim_id": 10, "ipm_share": "36000.00", "locked_at": "2026-03-04T04:30:43.520894+00:00", "total_amount": "45000.00", "patient_share": "9000.00", "medicine_names": "", "coverage_percent": "80.00"}	d22710682582f6b68c8a7698627f52678b48239853a8f13bf68ffe2ae24e36e5	2026-03-07 04:30:43.520955+00	2026-03-04 04:31:37.991579+00		2026-03-04 04:29:34.169107+00	2026-03-04 04:31:37.997643+00	1	6	4	2026-03-04	FAC-TEST-PROC-001	\N	f	\N	
12	READY_FOR_PAYMENT	35000.00		2026-03-04 05:50:56.814189+00	2026-03-04 05:50:56.818741+00	{"ipm": "IPM Horizon Santé", "formule": "Formule standard", "patient": "Awa Diop", "category": "Consultation", "claim_id": 12, "ipm_share": "28000.00", "locked_at": "2026-03-04T05:50:56.818720+00:00", "total_amount": "35000.00", "patient_share": "7000.00", "medicine_names": "", "coverage_percent": "80.00"}	424d3021da61963192d874a94dee03ec094adee5d3fd55c04187c0874bc4dbfd	2026-03-07 05:50:56.818766+00	2026-03-04 05:52:47.839836+00		2026-03-04 05:50:52.300614+00	2026-03-04 05:52:47.844276+00	1	6	5	2026-03-04	FAC-TEST-AWA-002	\N	f	\N	
\.


--
-- Data for Name: claims_claimauditlog; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_claimauditlog (id, event, notes, created_at, actor_id, claim_id) FROM stdin;
1	CLAIM_CREATED	Draft created	2026-02-15 20:16:09.241785+00	2	1
2	CLAIM_SUBMITTED	Claim submitted by provider	2026-02-15 20:16:20.440408+00	2	1
3	CLAIM_LOCKED	Snapshot generated and token issued	2026-02-15 20:17:04.484996+00	2	1
4	PATIENT_CONFIRMED	Patient confirmed snapshot	2026-02-15 20:17:21.795882+00	\N	1
5	READY_FOR_PAYMENT	Claim ready for payment	2026-02-15 20:17:21.797486+00	\N	1
6	CLAIM_SUBMITTED	Claim submitted by provider	2026-02-15 20:17:43.338783+00	2	2
7	CLAIM_LOCKED	Snapshot generated and token issued	2026-02-15 20:17:43.344536+00	2	2
8	CLAIM_BLOCKED	Auto blocked due to snapshot mismatch	2026-02-15 20:17:43.350636+00	\N	2
9	CLAIM_CREATED	Draft created	2026-02-20 01:54:23.347804+00	6	3
10	DOCUMENTS_UPLOADED	Remedi_logo_cropped.png	2026-02-20 01:54:23.363462+00	6	3
11	DOCUMENTS_UPLOADED	Remedi_logo_cropped.png	2026-02-20 01:54:23.375161+00	6	3
12	CLAIM_SUBMITTED	Claim submitted by provider	2026-02-20 01:54:47.620775+00	6	3
13	CLAIM_CREATED	Draft created	2026-02-20 02:11:53.728934+00	6	4
14	DOCUMENTS_UPLOADED	Remedi_logo_banner.png	2026-02-20 02:11:53.737471+00	6	4
15	CLAIM_SUBMITTED	Claim submitted by provider	2026-02-20 02:12:03.918412+00	6	4
16	CLAIM_LOCKED	Snapshot generated and token issued	2026-02-20 02:12:03.923841+00	6	4
17	PATIENT_DISPUTED	Patient disputed snapshot	2026-02-20 03:06:35.604431+00	\N	4
18	CLAIM_BLOCKED	Blocked after patient dispute	2026-02-20 03:06:35.613085+00	\N	4
19	CLAIM_CREATED	Draft created	2026-02-20 19:07:09.370295+00	6	5
20	CLAIM_CREATED	Draft created	2026-02-20 19:07:54.789532+00	6	6
21	DOCUMENTS_UPLOADED	Remedi_logo_banner.png	2026-02-20 19:07:54.797294+00	6	6
22	CLAIM_SUBMITTED	Claim submitted by provider	2026-02-20 19:07:59.079747+00	6	6
23	CLAIM_LOCKED	Snapshot generated and token issued	2026-02-20 19:07:59.089574+00	6	6
24	PATIENT_CONFIRMED	Patient confirmed snapshot	2026-02-20 19:09:30.665694+00	\N	6
25	READY_FOR_PAYMENT	Claim ready for payment	2026-02-20 19:09:30.66772+00	\N	6
26	CLAIM_CREATED	Draft created	2026-02-25 04:43:15.266565+00	6	7
27	CLAIM_CREATED	Draft created	2026-02-25 23:23:43.878608+00	6	8
28	DOCUMENTS_UPLOADED	Allergies and intolerance .pdf	2026-02-25 23:23:43.890817+00	6	8
29	CLAIM_CREATED	Draft created	2026-03-04 04:21:31.726504+00	4	9
30	CLAIM_LOCKED	Snapshot generated and token issued	2026-03-04 04:23:03.097981+00	4	9
31	CLAIM_CREATED	Draft created	2026-03-04 04:29:34.172252+00	6	10
32	CLAIM_LOCKED	Snapshot generated and token issued	2026-03-04 04:30:43.524616+00	4	10
33	PATIENT_CONFIRMED	Patient confirmed snapshot	2026-03-04 04:31:37.996082+00	\N	10
34	READY_FOR_PAYMENT	Claim ready for payment	2026-03-04 04:31:37.999103+00	\N	10
35	CLAIM_CREATED	Draft created	2026-03-04 05:48:44.193606+00	6	11
36	CLAIM_CREATED	Draft created	2026-03-04 05:50:52.309548+00	6	12
37	DOCUMENTS_UPLOADED	Logo_Ucad_Bleu.png	2026-03-04 05:50:52.318333+00	6	12
38	CLAIM_SUBMITTED	Claim submitted by provider	2026-03-04 05:50:56.815685+00	6	12
39	CLAIM_LOCKED	Snapshot generated and token issued	2026-03-04 05:50:56.820429+00	6	12
40	PATIENT_CONFIRMED	Patient confirmed snapshot	2026-03-04 05:52:47.843294+00	\N	12
41	READY_FOR_PAYMENT	Claim ready for payment	2026-03-04 05:52:47.845181+00	\N	12
\.


--
-- Data for Name: claims_claimdocument; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_claimdocument (id, file, original_name, uploaded_at, claim_id, document_type) FROM stdin;
1	claim_documents/2026/02/20/Remedi_logo_cropped.png	Remedi_logo_cropped.png	2026-02-20 01:54:23.36004+00	3	ORDONNANCE
2	claim_documents/2026/02/20/Remedi_logo_cropped_R1Wx1wo.png	Remedi_logo_cropped.png	2026-02-20 01:54:23.372903+00	3	FACTURE
3	claim_documents/2026/02/20/Remedi_logo_banner.png	Remedi_logo_banner.png	2026-02-20 02:11:53.735241+00	4	ORDONNANCE
4	claim_documents/2026/02/20/Remedi_logo_banner_dGuQDdn.png	Remedi_logo_banner.png	2026-02-20 19:07:54.794453+00	6	ORDONNANCE
5	claim_documents/2026/02/25/Allergies_and_intolerance_.pdf	Allergies and intolerance .pdf	2026-02-25 23:23:43.887386+00	8	ORDONNANCE
6	claim_documents/2026/03/04/Logo_Ucad_Bleu.png	Logo_Ucad_Bleu.png	2026-03-04 05:50:52.315554+00	12	ORDONNANCE
\.


--
-- Data for Name: claims_coverageplan; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_coverageplan (id, name, annual_ceiling, is_active, created_at, ipm_id) FROM stdin;
1	Formule Standard	\N	t	2026-02-19 23:58:26.870331+00	1
2	Formule standard	\N	t	2026-02-20 01:28:17.282011+00	2
3	VIP	\N	t	2026-02-22 23:28:16.347598+00	3
\.


--
-- Data for Name: claims_coveragerule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_coveragerule (id, coverage_percent, is_active, created_at, category_id, coverage_plan_id) FROM stdin;
1	70.00	t	2026-02-15 20:14:00.194107+00	1	1
2	60.00	t	2026-02-15 20:14:00.20662+00	2	1
3	80.00	t	2026-02-20 01:28:17.285382+00	16	2
4	80.00	t	2026-02-20 01:28:17.288596+00	8	2
5	80.00	t	2026-02-20 01:28:17.289628+00	15	2
6	80.00	t	2026-02-20 01:28:17.290423+00	7	2
7	80.00	t	2026-02-20 01:28:17.291233+00	26	2
8	80.00	t	2026-02-20 01:28:17.292013+00	1	2
9	80.00	t	2026-02-20 01:28:17.29285+00	3	2
10	80.00	t	2026-02-20 01:28:17.293706+00	4	2
11	80.00	t	2026-02-20 01:28:17.294634+00	25	2
12	80.00	t	2026-02-20 01:28:17.295392+00	11	2
13	80.00	t	2026-02-20 01:28:17.296151+00	5	2
14	80.00	t	2026-02-20 01:28:17.297034+00	13	2
15	80.00	t	2026-02-20 01:28:17.297856+00	9	2
16	80.00	t	2026-02-20 01:28:17.298813+00	21	2
17	80.00	t	2026-02-20 01:28:17.299656+00	14	2
18	80.00	t	2026-02-20 01:28:17.30046+00	19	2
19	80.00	t	2026-02-20 01:28:17.301388+00	24	2
20	80.00	t	2026-02-20 01:28:17.302234+00	23	2
21	80.00	t	2026-02-20 01:28:17.303038+00	18	2
22	80.00	t	2026-02-20 01:28:17.304079+00	20	2
23	80.00	t	2026-02-20 01:28:17.304866+00	2	2
24	80.00	t	2026-02-20 01:28:17.305605+00	10	2
25	80.00	t	2026-02-20 01:28:17.306315+00	12	2
26	80.00	t	2026-02-20 01:28:17.307071+00	17	2
27	80.00	t	2026-02-20 01:28:17.307828+00	6	2
28	80.00	t	2026-02-20 01:28:17.308582+00	22	2
29	50.00	t	2026-02-22 19:04:40.664412+00	15	1
30	95.00	t	2026-02-22 23:28:16.36295+00	16	3
31	95.00	t	2026-02-22 23:28:16.368985+00	8	3
32	95.00	t	2026-02-22 23:28:16.370515+00	15	3
33	95.00	t	2026-02-22 23:28:16.371523+00	7	3
34	95.00	t	2026-02-22 23:28:16.373643+00	26	3
35	95.00	t	2026-02-22 23:28:16.375162+00	1	3
36	100.00	t	2026-02-22 23:28:16.377515+00	3	3
37	95.00	t	2026-02-22 23:28:16.378618+00	4	3
38	95.00	t	2026-02-22 23:28:16.37996+00	25	3
39	95.00	t	2026-02-22 23:28:16.381083+00	11	3
40	95.00	t	2026-02-22 23:28:16.382209+00	5	3
41	95.00	t	2026-02-22 23:28:16.383117+00	13	3
42	95.00	t	2026-02-22 23:28:16.383868+00	9	3
43	95.00	t	2026-02-22 23:28:16.384932+00	21	3
44	95.00	t	2026-02-22 23:28:16.386669+00	14	3
45	95.00	t	2026-02-22 23:28:16.388709+00	19	3
46	95.00	t	2026-02-22 23:28:16.390325+00	24	3
47	100.00	t	2026-02-22 23:28:16.391334+00	23	3
48	95.00	t	2026-02-22 23:28:16.392411+00	18	3
49	95.00	t	2026-02-22 23:28:16.394444+00	20	3
50	95.00	t	2026-02-22 23:28:16.396386+00	2	3
51	95.00	t	2026-02-22 23:28:16.398191+00	10	3
52	95.00	t	2026-02-22 23:28:16.399349+00	12	3
53	95.00	t	2026-02-22 23:28:16.400759+00	17	3
54	95.00	t	2026-02-22 23:28:16.402789+00	6	3
55	95.00	t	2026-02-22 23:28:16.404515+00	22	3
\.


--
-- Data for Name: claims_establishmentpaymentoption; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_establishmentpaymentoption (id, is_deleted, deleted_at, phone, iban, bank_name, payee_name, reference_notes, is_active, created_at, deleted_by_id, hospital_id, payment_method_id) FROM stdin;
1	f	\N	221785962662					t	2026-02-23 04:59:02.886151+00	\N	1	4
2	f	\N	221785962662					t	2026-02-23 04:59:12.089601+00	\N	1	3
\.


--
-- Data for Name: claims_hospital; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_hospital (id, is_deleted, deleted_at, name, code, address, city, phone, email, is_active, created_at, updated_at, deleted_by_id, establishment_type) FROM stdin;
1	f	\N	Clinique Espoir	CliniqueEspoir					t	2026-02-20 02:55:12.091167+00	2026-02-20 02:55:12.091179+00	\N	HOSPITAL
2	f	\N	Ar-Rahma	PhAr	Route de Ouahigouya	Ouagadougou	77553322	zeinabsare892@gmail.com	t	2026-02-22 23:34:19.460156+00	2026-02-22 23:34:19.460166+00	\N	PHARMACY
3	f	\N	Pharmacie central	Pharmaciecentral					t	2026-02-23 04:26:47.881504+00	2026-02-23 04:26:47.88152+00	\N	PHARMACY
\.


--
-- Data for Name: claims_ipm; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_ipm (id, name, is_active, created_at, address, city, code, email, phone, updated_at, deleted_at, is_deleted, deleted_by_id) FROM stdin;
2	IPM Horizon Santé	t	2026-02-20 01:13:12.076443+00	12 Avenue de la République	Dakar	HORIZON	contact@ipm-horizon.sn	221 77 000 00 02	2026-03-04 04:16:47.342314+00	\N	f	\N
1	IPM SANTE PLUS	t	2026-02-15 20:14:00.115999+00	25 Avenue Léopold Sédar Senghor	Dakar	SANTEPLUS	contact@ipm-santeplus.sn	221 33 859 00 01	2026-03-04 04:17:17.087672+00	\N	f	\N
3	Zeinsanté	t	2026-02-22 18:59:05.448984+00	8 Rue du Commerce	Dakar	ZEINSANTE	contact@zeinsante.sn	221 33 821 00 03	2026-03-04 04:17:35.437404+00	\N	f	\N
\.


--
-- Data for Name: claims_ipmpaymentoption; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_ipmpaymentoption (id, phone, iban, bank_name, payee_name, reference_notes, is_active, created_at, ipm_id, payment_method_id, deleted_at, is_deleted, deleted_by_id) FROM stdin;
1						t	2026-02-20 01:51:52.89408+00	2	2	\N	f	\N
\.


--
-- Data for Name: claims_notificationchannelconfig; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_notificationchannelconfig (id, channel, is_active, config, last_tested_at, last_test_error) FROM stdin;
1	SMS	f	{}	\N	
2	WHATSAPP	f	{}	\N	
3	EMAIL	t	{"host": "smtp.hostinger.com", "port": 465, "user": "otp@tickets-place.net", "use_ssl": true, "use_tls": false, "password": "qF~2SdAiP*A", "from_email": "otp@tickets-place.net", "body_template": "", "subject_template": "[REMEDY] Votre réclamation à valider"}	2026-02-20 18:44:36.072567+00	
\.


--
-- Data for Name: claims_notificationlog; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_notificationlog (id, channel, target, sent_at, status, claim_id, error_message) FROM stdin;
1	EMAIL	aboubacarsawadogo15@gmail.com	2026-02-20 19:08:59.69456+00	SENT	6	
2	EMAIL	moussa.diop@exemple.sn	2026-03-04 04:23:05.408471+00	SENT	9	
3	EMAIL	seynabou.fall@exemple.sn	2026-03-04 04:30:44.113664+00	SENT	10	
4	EMAIL	awa.diop@exemple.sn	2026-03-04 05:50:57.308567+00	SENT	12	
\.


--
-- Data for Name: claims_patient; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_patient (id, full_name, phone, member_number, created_at, ipm_id, beneficiary_type, coverage_plan_id, address, city, date_of_birth, email, gender, id_number, notes, updated_at, id_document) FROM stdin;
1	Moussa Diop	+221 77 101 00 01	M-1001	2026-02-15 20:14:00.129128+00	1	TITULAIRE	1			\N	moussa.diop@exemple.sn				2026-03-04 04:18:05.228297+00	
2	Aicha Ndiaye	+221 77 101 00 02	M-1002	2026-02-15 20:14:00.168303+00	1	TITULAIRE	1			\N	aicha.ndiaye@exemple.sn				2026-03-04 04:18:26.271535+00	
3	Ousmane Diallo	+221 77 101 00 03	M-2001	2026-02-20 01:30:38.507982+00	2	TITULAIRE	2	12 Avenue de la République	Dakar	2026-01-26	ousmane.diallo@exemple.sn	M	CNI-DEMO-2001	Données de démonstration	2026-03-04 04:18:45.378259+00	patient_kyc/2026/02/Logo_Remedi_-_Sante_Digitale_Simplifiee.png
4	Seynabou Fall	+221 77 102 00 01	M-2002	2026-03-04 04:28:12.938688+00	2	TITULAIRE	2			\N	seynabou.fall@exemple.sn				2026-03-04 04:28:12.938702+00	
5	Awa Diop	+221 77 102 00 02	M-3001	2026-03-04 05:38:31.365449+00	2	TITULAIRE	2			\N	awa.diop@exemple.sn				2026-03-04 05:38:31.36546+00	
\.


--
-- Data for Name: claims_paymentmethod; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.claims_paymentmethod (id, name, code, is_active, created_at, method_type) FROM stdin;
2	CHEQUE	CHEQUE	t	2026-02-20 00:20:26.234942+00	CHEQUE
4	Orange Money	ORANGE_MONEY	t	2026-02-20 00:20:41.501226+00	MOBILE_MONEY
1	Virement bancaire	VIREMENT_BANCAIRE	t	2026-02-20 00:20:17.115227+00	VIREMENT
3	Wave	WAVE	t	2026-02-20 00:20:32.379489+00	MOBILE_MONEY
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2026-02-20 02:10:53.157019+00	3	Claim #3 - SUBMITTED	2	[]	9	4
2	2026-02-20 02:11:08.342747+00	3	Claim #3 - SUBMITTED	3		9	4
3	2026-03-04 04:22:35.659876+00	9	Claim #9 - SUBMITTED	2	[{"changed": {"fields": ["Status"]}}]	9	4
4	2026-03-04 04:23:59.82576+00	9	Claim #9 - READY_FOR_PAYMENT	2	[{"changed": {"fields": ["Status"]}}]	9	4
5	2026-03-04 04:30:26.199702+00	10	Claim #10 - SUBMITTED	2	[{"changed": {"fields": ["Status"]}}]	9	4
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	accounts	staffprofile
8	claims	category
9	claims	claim
10	claims	claimauditlog
11	claims	claimdocument
12	claims	coveragerule
13	claims	ipm
14	claims	notificationlog
15	claims	patient
16	claims	coverageplan
17	claims	paymentmethod
18	claims	ipmpaymentoption
19	claims	hospital
20	claims	notificationchannelconfig
21	claims	establishmentpaymentoption
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-02-15 20:13:46.954652+00
2	auth	0001_initial	2026-02-15 20:13:47.046161+00
3	accounts	0001_initial	2026-02-15 20:13:47.061554+00
4	admin	0001_initial	2026-02-15 20:13:47.082382+00
5	admin	0002_logentry_remove_auto_add	2026-02-15 20:13:47.088423+00
6	admin	0003_logentry_add_action_flag_choices	2026-02-15 20:13:47.09396+00
7	contenttypes	0002_remove_content_type_name	2026-02-15 20:13:47.108212+00
8	auth	0002_alter_permission_name_max_length	2026-02-15 20:13:47.117053+00
9	auth	0003_alter_user_email_max_length	2026-02-15 20:13:47.124247+00
10	auth	0004_alter_user_username_opts	2026-02-15 20:13:47.130992+00
11	auth	0005_alter_user_last_login_null	2026-02-15 20:13:47.140285+00
12	auth	0006_require_contenttypes_0002	2026-02-15 20:13:47.142511+00
13	auth	0007_alter_validators_add_error_messages	2026-02-15 20:13:47.148775+00
14	auth	0008_alter_user_username_max_length	2026-02-15 20:13:47.161845+00
15	auth	0009_alter_user_last_name_max_length	2026-02-15 20:13:47.172546+00
16	auth	0010_alter_group_name_max_length	2026-02-15 20:13:47.18275+00
17	auth	0011_update_proxy_permissions	2026-02-15 20:13:47.189617+00
18	auth	0012_alter_user_first_name_max_length	2026-02-15 20:13:47.197054+00
19	claims	0001_initial	2026-02-15 20:13:47.340872+00
20	sessions	0001_initial	2026-02-15 20:13:47.355042+00
21	claims	0002_add_care_date_invoice_document_type	2026-02-15 21:34:26.125615+00
22	claims	0003_coverage_plan_refactor	2026-02-19 23:58:26.853695+00
23	claims	0004_populate_coverage_plans	2026-02-19 23:58:26.877915+00
24	claims	0005_remove_coveragerule_ipm_finalize	2026-02-19 23:58:26.914619+00
25	claims	0006_ipm_enrich_fields	2026-02-20 00:11:32.729966+00
26	claims	0007_ipm_code_nullable	2026-02-20 00:13:52.033151+00
27	claims	0008_add_payment_method	2026-02-20 00:16:10.928834+00
28	claims	0009_payment_method_type_and_ipm_options	2026-02-20 00:23:18.579208+00
29	claims	0010_soft_delete_claim_ipmpaymentoption	2026-02-20 00:30:56.296403+00
30	accounts	0002_soft_delete_ipm_staffprofile	2026-02-20 00:40:34.726455+00
31	claims	0011_soft_delete_ipm_staffprofile	2026-02-20 00:40:34.770867+00
32	accounts	0003_add_deleted_by	2026-02-20 00:54:44.444813+00
33	claims	0012_add_deleted_by	2026-02-20 00:54:44.501631+00
34	claims	0013_patient_enrich_fields	2026-02-20 01:32:49.214809+00
35	claims	0014_patient_kyc_id_document	2026-02-20 01:35:03.802593+00
36	accounts	0004_add_organisation_name	2026-02-20 02:23:23.066339+00
37	claims	0015_add_hospital	2026-02-20 02:31:53.626979+00
38	accounts	0005_add_hospital_fk	2026-02-20 02:31:53.660443+00
39	claims	0016_hospital_type_and_dispute_reason	2026-02-20 02:35:28.184962+00
40	claims	0017_notification_channel_config	2026-02-20 03:17:37.759749+00
41	claims	0018_notification_log_error_and_target	2026-02-20 18:18:12.945526+00
42	claims	0019_establishment_payment_options	2026-02-20 19:13:19.23026+00
43	accounts	0006_add_staffprofile_ipm_fk	2026-02-23 04:20:08.601514+00
44	accounts	0007_alter_staffprofile_ipm_name	2026-02-23 04:43:56.817179+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
p30wv3iz6l99ej85xnkt1pwq83tjjpes	.eJxVjMEOwiAQBf-FsyFAgQWP3vsNhIWtVA0kpT0Z_92Q9KDXNzPvzUI89hKOTltYM7syxS6_G8b0pDpAfsR6bzy1um8r8qHwk3Y-t0yv2-n-HZTYy6gdTQ6tnAAlYdIiI1gERTEnD8IYiQhSe6NJe7KakMAJgdlZtUizsM8X73o4Cg:1vriWo:xgCrrnhkjpk1Afo2xSihy8BK1FJZ0iJi8X_2QmZHULY	2026-03-01 20:15:38.848505+00
45ow65two261njhvvx64denn3gs9h9c4	.eJxVjDsOwjAQBe_iGln-xY4p6TmDtetd4wBypDipEHeHSCmgfTPzXiLBtta0dV7SROIstDj9bgj5wW0HdId2m2We27pMKHdFHrTL60z8vBzu30GFXr81WAvaOU9GK1MiFhM0ZYs6l4CR0bNGHoKh0ZUc_TiQtwpUcQ48BJPF-wPpHjgj:1vrjn9:OTy6WhdSe34dL1LiXZ13GKWZzRKb-vKnJnBmtSW_Yws	2026-03-01 21:36:35.673234+00
v8gy4le2cy75q479x0m82xktu0qsqk5n	.eJxVjDsOwjAQBe_iGlm240-Wkj5nsNbeNQkgR4qTCnF3EikFtG9m3ltE3NYxbo2XOJG4il5cfreE-cn1APTAep9lnuu6TEkeijxpk8NM_Lqd7t_BiG3ca2Z2NlimQgUBoIdE2bnQdey81goyJpONh6AJut7uUjbKKEC0yhcjPl__PDfs:1vtW6w:_ysZQns8XCyOsd2SmknE2lzQQqyCx2MoMZGqdbkLJKk	2026-03-06 19:24:22.078786+00
yzdieedh4wzmpmluqop9uafgs2dyaw2t	.eJxVjDsOwjAQBe_iGln-xY4p6TmDtetd4wBypDipEHeHSCmgfTPzXiLBtta0dV7SROIstDj9bgj5wW0HdId2m2We27pMKHdFHrTL60z8vBzu30GFXr81WAvaOU9GK1MiFhM0ZYs6l4CR0bNGHoKh0ZUc_TiQtwpUcQ48BJPF-wPpHjgj:1vrjqP:ZrlDgl7JdNXf9wMKEBbhJN4Chth4AP-_QvJgYlrNgL4	2026-03-01 21:39:57.37702+00
jsqs5x36svxzqpcsl4blnko07k8ny743	.eJxVjDsOwjAQBe_iGln-xY4p6TmDtetd4wBypDipEHeHSCmgfTPzXiLBtta0dV7SROIstDj9bgj5wW0HdId2m2We27pMKHdFHrTL60z8vBzu30GFXr81WAvaOU9GK1MiFhM0ZYs6l4CR0bNGHoKh0ZUc_TiQtwpUcQ48BJPF-wPpHjgj:1vtXQv:ztqHaIkp5JRTbACzkVJhuGyCFFkBboJMrzqavySSr_Q	2026-03-06 20:49:05.138691+00
dmytodcybqi3ry63sgs4bccdkjmrc1o8	.eJxVjDsOwyAQRO9CHSE-Np-U6X0GtMtCcBKBZOwqyt1jSy6SbjTvzbxZgG0tYetpCTOxKxvY5bdDiM9UD0APqPfGY6vrMiM_FH7SzqdG6XU73b-DAr3s6-SF8iInSeBGGzVJA2StzNYqr8FFdITaZXQpO1R7NlEYo2AgNXq07PMF8eg4RQ:1vtDuI:j2Rzps8gb-N1C1A1yi2mI71hE0xXfTvMxy05hGR_H8c	2026-03-05 23:58:06.217699+00
d3q9t70mpfjw26mywgkri6t74zqhh3m8	.eJxVjEEOwiAQRe_C2hAoHaQu3fcMzQwzSNVAUtqV8e7apAvd_vfef6kJtzVPW5NlmlldFKjT70YYH1J2wHcst6pjLesyk94VfdCmx8ryvB7u30HGlr81EgdnO4ypTz6dBcIA1nSOIXgDhgQNBYMANoQe2UtiMimxs0N0QKjeH-2VOFg:1vxfAv:Pd_Vabp4BZpxjGLdZlMSortixDFiOMElvP3FXglesuw	2026-03-18 05:53:37.686742+00
187x7hwl1iimbwgt01k83ultr4jt98bk	.eJxVjDsOwyAQRO9CHSE-Np-U6X0GtMtCcBKBZOwqyt1jSy6SbjTvzbxZgG0tYetpCTOxKxvY5bdDiM9UD0APqPfGY6vrMiM_FH7SzqdG6XU73b-DAr3s6-SF8iInSeBGGzVJA2StzNYqr8FFdITaZXQpO1R7NlEYo2AgNXq07PMF8eg4RQ:1vuKZn:nfRRgpYyiTzcU_dHGe0JUeGDojr98D4KsQ_hUsCPVoQ	2026-03-09 01:17:31.075742+00
k5r25fciva7995wg7b9vybef32itgl56	.eJxVjEEOgjAQRe_StWlqYVrq0j1nIDOdGYsaSCisjHdXEha6_e-9_zIDbmsZtirLMLK5mGBOvxthfsi0A77jdJttnqd1Gcnuij1otf3M8rwe7t9BwVq-NWRxCZlEXRcZPEJLngRjiiAamtAoAYekmtvctSE5FlAHXs5J0Kl5fwAN0jja:1vuNKA:dtI4xKWRnf8vMUcdPTbRZDJ-l26QJEqdWcp-iAtof5I	2026-03-09 04:13:34.497415+00
fe285e3cni3zpm63h3zcxxrgwe4sqtlf	.eJxVjDsOwyAQRO9CHSE-Np-U6X0GtMtCcBKBZOwqyt1jSy6SbjTvzbxZgG0tYetpCTOxKxvY5bdDiM9UD0APqPfGY6vrMiM_FH7SzqdG6XU73b-DAr3s6-SF8iInSeBGGzVJA2StzNYqr8FFdITaZXQpO1R7NlEYo2AgNXq07PMF8eg4RQ:1vugVV:RqhmfqA386ROlqDmzNx7UFtRFrOF8nwbLl-MJo067Es	2026-03-10 00:42:33.602094+00
dwh7yf8rwv08waxc7n1t31j86mrq41h7	.eJxVjDsOwyAQRO9CHSE-Np-U6X0GtMtCcBKBZOwqyt1jSy6SbjTvzbxZgG0tYetpCTOxKxvY5bdDiM9UD0APqPfGY6vrMiM_FH7SzqdG6XU73b-DAr3s6-SF8iInSeBGGzVJA2StzNYqr8FFdITaZXQpO1R7NlEYo2AgNXq07PMF8eg4RQ:1vv6Th:Qx6w90DFYuSXhypa9j_Vp1T3bdGT7TQWO3j6IWpLhhU	2026-03-11 04:26:25.303361+00
28l4lf3gvqejzdk6calwbnzraxzl2e9k	.eJxVjDsOwyAQRO9CHSE-Np-U6X0GtMtCcBKBZOwqyt1jSy6SbjTvzbxZgG0tYetpCTOxKxvY5bdDiM9UD0APqPfGY6vrMiM_FH7SzqdG6XU73b-DAr3s6-SF8iInSeBGGzVJA2StzNYqr8FFdITaZXQpO1R7NlEYo2AgNXq07PMF8eg4RQ:1vtHAH:72teq0g9X8ema75rb1qD7L2Iyv-qoH5Rq_qYGrdzqro	2026-03-06 03:26:49.139964+00
ez87r581ma46fbyt9db1qqn5mab8se8a	.eJxVjEEOwiAQRe_C2hAoHaQu3fcMzQwzSNVAUtqV8e7apAvd_vfef6kJtzVPW5NlmlldFKjT70YYH1J2wHcst6pjLesyk94VfdCmx8ryvB7u30HGlr81EgdnO4ypTz6dBcIA1nSOIXgDhgQNBYMANoQe2UtiMimxs0N0QKjeH-2VOFg:1vv6Ts:ThkxqgD4hJeaFg47Kr-UIdrwGbgkNiafYCn3moeoCVs	2026-03-11 04:26:36.811353+00
g7tw3q7kwhmtxlmn4piyyl8l1wuhq6j6	.eJxVjEEOgjAQRe_StWlqYVrq0j1nIDOdGYsaSCisjHdXEha6_e-9_zIDbmsZtirLMLK5mGBOvxthfsi0A77jdJttnqd1Gcnuij1otf3M8rwe7t9BwVq-NWRxCZlEXRcZPEJLngRjiiAamtAoAYekmtvctSE5FlAHXs5J0Kl5fwAN0jja:1vv6U0:Au9Okb29EG_ZRbcaHHGwoUI6RPenQk734DGC6mcKQKA	2026-03-11 04:26:44.331717+00
8im1uwyxmqmyn8tqlcx99jf1u7b4h7ae	.eJxVjEEOwiAQRe_C2hCYKYW6dN8zkGEYbdVAUtqV8e7apAvd_vfef6lI2zrFrckS56zOyqvT75aIH1J2kO9UblVzLesyJ70r-qBNjzXL83K4fwcTtelbW2ILLqEAJiMECGwMcu9CQGa-2gFFsveWKAyE1HsHHUPnqQdAIfX-AOJVN7I:1vv6UA:l1XwgoP1cf0q0xwaFrGQGJa0m5pFeilmuNhrzo7guEI	2026-03-11 04:26:54.906427+00
dvchnzg6i84d597a4ip61effu2eqz25g	.eJxVjDsOwyAQRO9CHSE-Np-U6X0GtMtCcBKBZOwqyt1jSy6SbjTvzbxZgG0tYetpCTOxKxvY5bdDiM9UD0APqPfGY6vrMiM_FH7SzqdG6XU73b-DAr3s6-SF8iInSeBGGzVJA2StzNYqr8FFdITaZXQpO1R7NlEYo2AgNXq07PMF8eg4RQ:1vv6fb:muyfyhU8G-lQbrg3sXuHPHzNSZ1WLlTNUE04OKf2owg	2026-03-11 04:38:43.843748+00
p5ailr7i2vwii37o6lbyazwmo7ocx2rm	.eJxVjEEOwiAQRe_C2hAoHaQu3fcMzQwzSNVAUtqV8e7apAvd_vfef6kJtzVPW5NlmlldFKjT70YYH1J2wHcst6pjLesyk94VfdCmx8ryvB7u30HGlr81EgdnO4ypTz6dBcIA1nSOIXgDhgQNBYMANoQe2UtiMimxs0N0QKjeH-2VOFg:1vv6gC:qd6d3R7XFebFTQJpCZcw3gwojOVv_fD5xTKrbGW-F_o	2026-03-11 04:39:20.620953+00
n4950fkpnli1nisqqt6vgkdqnqocrz7k	.eJxVjEEOgjAQRe_StWlqYVrq0j1nIDOdGYsaSCisjHdXEha6_e-9_zIDbmsZtirLMLK5mGBOvxthfsi0A77jdJttnqd1Gcnuij1otf3M8rwe7t9BwVq-NWRxCZlEXRcZPEJLngRjiiAamtAoAYekmtvctSE5FlAHXs5J0Kl5fwAN0jja:1vv6gc:W_zkhy_-DJnhm672iHOGA73IbVMZBweZA5V3loKb31Y	2026-03-11 04:39:46.869614+00
i12b9d2thiytlw9nhymzbdgi1lnb80ov	.eJxVjDsOwjAQBe_iGln-xY4p6TmDtetd4wBypDipEHeHSCmgfTPzXiLBtta0dV7SROIstDj9bgj5wW0HdId2m2We27pMKHdFHrTL60z8vBzu30GFXr81WAvaOU9GK1MiFhM0ZYs6l4CR0bNGHoKh0ZUc_TiQtwpUcQ48BJPF-wPpHjgj:1vtW3A:SfiVa20FfNRD0oOUiEI42U5qUIzmRfrYgkTYScnzG_o	2026-03-06 19:20:28.812283+00
eppuowiq70k6phuffqwoky8p00cxylu4	.eJxVjDsOwjAQBe_iGln-xY4p6TmDtetd4wBypDipEHeHSCmgfTPzXiLBtta0dV7SROIstDj9bgj5wW0HdId2m2We27pMKHdFHrTL60z8vBzu30GFXr81WAvaOU9GK1MiFhM0ZYs6l4CR0bNGHoKh0ZUc_TiQtwpUcQ48BJPF-wPpHjgj:1vtW3K:BGdmmfuhLNE3Pvv_FwYCHbhBj0CY-SYrVQ4tYQSJa7U	2026-03-06 19:20:38.561412+00
jfh4fsnk4hbrf77c4ov1qznpp3a5hyac	.eJxVjEEOwiAQRe_C2hAoHaQu3fcMzQwzSNVAUtqV8e7apAvd_vfef6kJtzVPW5NlmlldFKjT70YYH1J2wHcst6pjLesyk94VfdCmx8ryvB7u30HGlr81EgdnO4ypTz6dBcIA1nSOIXgDhgQNBYMANoQe2UtiMimxs0N0QKjeH-2VOFg:1vvOFW:9YEvoK7i6NrZ7k1MGScQZuJw8D-ncWIEDfoWjCOFjHE	2026-03-11 23:24:58.517046+00
\.


--
-- Name: accounts_staffprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_staffprofile_id_seq', 8, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 84, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 8, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: claims_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_category_id_seq', 26, true);


--
-- Name: claims_claim_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_claim_id_seq', 12, true);


--
-- Name: claims_claimauditlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_claimauditlog_id_seq', 41, true);


--
-- Name: claims_claimdocument_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_claimdocument_id_seq', 6, true);


--
-- Name: claims_coverageplan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_coverageplan_id_seq', 3, true);


--
-- Name: claims_coveragerule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_coveragerule_id_seq', 55, true);


--
-- Name: claims_establishmentpaymentoption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_establishmentpaymentoption_id_seq', 2, true);


--
-- Name: claims_hospital_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_hospital_id_seq', 3, true);


--
-- Name: claims_ipm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_ipm_id_seq', 3, true);


--
-- Name: claims_ipmpaymentoption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_ipmpaymentoption_id_seq', 1, true);


--
-- Name: claims_notificationchannelconfig_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_notificationchannelconfig_id_seq', 3, true);


--
-- Name: claims_notificationlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_notificationlog_id_seq', 4, true);


--
-- Name: claims_patient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_patient_id_seq', 5, true);


--
-- Name: claims_paymentmethod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.claims_paymentmethod_id_seq', 4, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 5, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 21, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 44, true);


--
-- Name: accounts_staffprofile accounts_staffprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_staffprofile
    ADD CONSTRAINT accounts_staffprofile_pkey PRIMARY KEY (id);


--
-- Name: accounts_staffprofile accounts_staffprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_staffprofile
    ADD CONSTRAINT accounts_staffprofile_user_id_key UNIQUE (user_id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: claims_category claims_category_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_category
    ADD CONSTRAINT claims_category_name_key UNIQUE (name);


--
-- Name: claims_category claims_category_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_category
    ADD CONSTRAINT claims_category_pkey PRIMARY KEY (id);


--
-- Name: claims_claim claims_claim_patient_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claim
    ADD CONSTRAINT claims_claim_patient_token_key UNIQUE (patient_token);


--
-- Name: claims_claim claims_claim_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claim
    ADD CONSTRAINT claims_claim_pkey PRIMARY KEY (id);


--
-- Name: claims_claimauditlog claims_claimauditlog_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claimauditlog
    ADD CONSTRAINT claims_claimauditlog_pkey PRIMARY KEY (id);


--
-- Name: claims_claimdocument claims_claimdocument_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claimdocument
    ADD CONSTRAINT claims_claimdocument_pkey PRIMARY KEY (id);


--
-- Name: claims_coverageplan claims_coverageplan_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_coverageplan
    ADD CONSTRAINT claims_coverageplan_pkey PRIMARY KEY (id);


--
-- Name: claims_coveragerule claims_coveragerule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_coveragerule
    ADD CONSTRAINT claims_coveragerule_pkey PRIMARY KEY (id);


--
-- Name: claims_establishmentpaymentoption claims_establishmentpaymentoption_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_establishmentpaymentoption
    ADD CONSTRAINT claims_establishmentpaymentoption_pkey PRIMARY KEY (id);


--
-- Name: claims_hospital claims_hospital_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_hospital
    ADD CONSTRAINT claims_hospital_pkey PRIMARY KEY (id);


--
-- Name: claims_ipm claims_ipm_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_ipm
    ADD CONSTRAINT claims_ipm_pkey PRIMARY KEY (id);


--
-- Name: claims_ipmpaymentoption claims_ipmpaymentoption_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_ipmpaymentoption
    ADD CONSTRAINT claims_ipmpaymentoption_pkey PRIMARY KEY (id);


--
-- Name: claims_notificationchannelconfig claims_notificationchannelconfig_channel_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_notificationchannelconfig
    ADD CONSTRAINT claims_notificationchannelconfig_channel_key UNIQUE (channel);


--
-- Name: claims_notificationchannelconfig claims_notificationchannelconfig_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_notificationchannelconfig
    ADD CONSTRAINT claims_notificationchannelconfig_pkey PRIMARY KEY (id);


--
-- Name: claims_notificationlog claims_notificationlog_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_notificationlog
    ADD CONSTRAINT claims_notificationlog_pkey PRIMARY KEY (id);


--
-- Name: claims_patient claims_patient_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_patient
    ADD CONSTRAINT claims_patient_pkey PRIMARY KEY (id);


--
-- Name: claims_paymentmethod claims_paymentmethod_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_paymentmethod
    ADD CONSTRAINT claims_paymentmethod_code_key UNIQUE (code);


--
-- Name: claims_paymentmethod claims_paymentmethod_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_paymentmethod
    ADD CONSTRAINT claims_paymentmethod_name_key UNIQUE (name);


--
-- Name: claims_paymentmethod claims_paymentmethod_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_paymentmethod
    ADD CONSTRAINT claims_paymentmethod_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: claims_coveragerule unique_coverage_per_plan_category; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_coveragerule
    ADD CONSTRAINT unique_coverage_per_plan_category UNIQUE (coverage_plan_id, category_id);


--
-- Name: claims_patient unique_patient_per_ipm; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_patient
    ADD CONSTRAINT unique_patient_per_ipm UNIQUE (ipm_id, member_number);


--
-- Name: claims_coverageplan unique_plan_per_ipm; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_coverageplan
    ADD CONSTRAINT unique_plan_per_ipm UNIQUE (ipm_id, name);


--
-- Name: accounts_staffprofile_deleted_by_id_87c58fb0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_staffprofile_deleted_by_id_87c58fb0 ON public.accounts_staffprofile USING btree (deleted_by_id);


--
-- Name: accounts_staffprofile_hospital_id_465f1649; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_staffprofile_hospital_id_465f1649 ON public.accounts_staffprofile USING btree (hospital_id);


--
-- Name: accounts_staffprofile_ipm_id_ba365394; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX accounts_staffprofile_ipm_id_ba365394 ON public.accounts_staffprofile USING btree (ipm_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: claims_category_name_42e04624_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_category_name_42e04624_like ON public.claims_category USING btree (name varchar_pattern_ops);


--
-- Name: claims_claim_category_id_872bdf1a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_claim_category_id_872bdf1a ON public.claims_claim USING btree (category_id);


--
-- Name: claims_claim_deleted_by_id_162ba72d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_claim_deleted_by_id_162ba72d ON public.claims_claim USING btree (deleted_by_id);


--
-- Name: claims_claim_patient_id_c2aa2b02; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_claim_patient_id_c2aa2b02 ON public.claims_claim USING btree (patient_id);


--
-- Name: claims_claim_patient_token_3e5d3564_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_claim_patient_token_3e5d3564_like ON public.claims_claim USING btree (patient_token varchar_pattern_ops);


--
-- Name: claims_claim_provider_id_45721be3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_claim_provider_id_45721be3 ON public.claims_claim USING btree (provider_id);


--
-- Name: claims_claimauditlog_actor_id_1101d5f7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_claimauditlog_actor_id_1101d5f7 ON public.claims_claimauditlog USING btree (actor_id);


--
-- Name: claims_claimauditlog_claim_id_1275ed2d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_claimauditlog_claim_id_1275ed2d ON public.claims_claimauditlog USING btree (claim_id);


--
-- Name: claims_claimdocument_claim_id_c1c69bf4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_claimdocument_claim_id_c1c69bf4 ON public.claims_claimdocument USING btree (claim_id);


--
-- Name: claims_coverageplan_ipm_id_33660a0a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_coverageplan_ipm_id_33660a0a ON public.claims_coverageplan USING btree (ipm_id);


--
-- Name: claims_coveragerule_category_id_3ce30a5e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_coveragerule_category_id_3ce30a5e ON public.claims_coveragerule USING btree (category_id);


--
-- Name: claims_coveragerule_coverage_plan_id_289a27db; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_coveragerule_coverage_plan_id_289a27db ON public.claims_coveragerule USING btree (coverage_plan_id);


--
-- Name: claims_establishmentpaymentoption_deleted_by_id_d16cf8e7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_establishmentpaymentoption_deleted_by_id_d16cf8e7 ON public.claims_establishmentpaymentoption USING btree (deleted_by_id);


--
-- Name: claims_establishmentpaymentoption_hospital_id_ca790a41; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_establishmentpaymentoption_hospital_id_ca790a41 ON public.claims_establishmentpaymentoption USING btree (hospital_id);


--
-- Name: claims_establishmentpaymentoption_payment_method_id_0587b8c6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_establishmentpaymentoption_payment_method_id_0587b8c6 ON public.claims_establishmentpaymentoption USING btree (payment_method_id);


--
-- Name: claims_hospital_deleted_by_id_43fdc6f4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_hospital_deleted_by_id_43fdc6f4 ON public.claims_hospital USING btree (deleted_by_id);


--
-- Name: claims_ipm_deleted_by_id_8022a2c0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_ipm_deleted_by_id_8022a2c0 ON public.claims_ipm USING btree (deleted_by_id);


--
-- Name: claims_ipmpaymentoption_deleted_by_id_0ec82b0e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_ipmpaymentoption_deleted_by_id_0ec82b0e ON public.claims_ipmpaymentoption USING btree (deleted_by_id);


--
-- Name: claims_ipmpaymentoption_ipm_id_cb509215; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_ipmpaymentoption_ipm_id_cb509215 ON public.claims_ipmpaymentoption USING btree (ipm_id);


--
-- Name: claims_ipmpaymentoption_payment_method_id_7fbb0924; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_ipmpaymentoption_payment_method_id_7fbb0924 ON public.claims_ipmpaymentoption USING btree (payment_method_id);


--
-- Name: claims_notificationchannelconfig_channel_a957fde6_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_notificationchannelconfig_channel_a957fde6_like ON public.claims_notificationchannelconfig USING btree (channel varchar_pattern_ops);


--
-- Name: claims_notificationlog_claim_id_b6e75016; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_notificationlog_claim_id_b6e75016 ON public.claims_notificationlog USING btree (claim_id);


--
-- Name: claims_patient_coverage_plan_id_6d4b902e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_patient_coverage_plan_id_6d4b902e ON public.claims_patient USING btree (coverage_plan_id);


--
-- Name: claims_patient_ipm_id_6942c307; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_patient_ipm_id_6942c307 ON public.claims_patient USING btree (ipm_id);


--
-- Name: claims_paymentmethod_code_203ec9c4_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_paymentmethod_code_203ec9c4_like ON public.claims_paymentmethod USING btree (code varchar_pattern_ops);


--
-- Name: claims_paymentmethod_name_b977624f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX claims_paymentmethod_name_b977624f_like ON public.claims_paymentmethod USING btree (name varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: unique_establishment_payment_option; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_establishment_payment_option ON public.claims_establishmentpaymentoption USING btree (hospital_id, payment_method_id) WHERE (NOT is_deleted);


--
-- Name: unique_hospital_code_not_deleted; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_hospital_code_not_deleted ON public.claims_hospital USING btree (code) WHERE ((NOT is_deleted) AND (NOT (((code)::text = ''::text) AND (code IS NOT NULL))));


--
-- Name: unique_hospital_name_not_deleted; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_hospital_name_not_deleted ON public.claims_hospital USING btree (name) WHERE (NOT is_deleted);


--
-- Name: unique_ipm_code_not_deleted; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_ipm_code_not_deleted ON public.claims_ipm USING btree (code) WHERE ((NOT is_deleted) AND (NOT (((code)::text = ''::text) AND (code IS NOT NULL))));


--
-- Name: unique_ipm_name_not_deleted; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_ipm_name_not_deleted ON public.claims_ipm USING btree (name) WHERE (NOT is_deleted);


--
-- Name: unique_ipm_payment_option; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_ipm_payment_option ON public.claims_ipmpaymentoption USING btree (ipm_id, payment_method_id) WHERE (NOT is_deleted);


--
-- Name: accounts_staffprofile accounts_staffprofil_hospital_id_465f1649_fk_claims_ho; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_staffprofile
    ADD CONSTRAINT accounts_staffprofil_hospital_id_465f1649_fk_claims_ho FOREIGN KEY (hospital_id) REFERENCES public.claims_hospital(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_staffprofile accounts_staffprofile_deleted_by_id_87c58fb0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_staffprofile
    ADD CONSTRAINT accounts_staffprofile_deleted_by_id_87c58fb0_fk_auth_user_id FOREIGN KEY (deleted_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_staffprofile accounts_staffprofile_ipm_id_ba365394_fk_claims_ipm_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_staffprofile
    ADD CONSTRAINT accounts_staffprofile_ipm_id_ba365394_fk_claims_ipm_id FOREIGN KEY (ipm_id) REFERENCES public.claims_ipm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_staffprofile accounts_staffprofile_user_id_1ed1af60_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts_staffprofile
    ADD CONSTRAINT accounts_staffprofile_user_id_1ed1af60_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_claim claims_claim_category_id_872bdf1a_fk_claims_category_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claim
    ADD CONSTRAINT claims_claim_category_id_872bdf1a_fk_claims_category_id FOREIGN KEY (category_id) REFERENCES public.claims_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_claim claims_claim_deleted_by_id_162ba72d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claim
    ADD CONSTRAINT claims_claim_deleted_by_id_162ba72d_fk_auth_user_id FOREIGN KEY (deleted_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_claim claims_claim_patient_id_c2aa2b02_fk_claims_patient_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claim
    ADD CONSTRAINT claims_claim_patient_id_c2aa2b02_fk_claims_patient_id FOREIGN KEY (patient_id) REFERENCES public.claims_patient(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_claim claims_claim_provider_id_45721be3_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claim
    ADD CONSTRAINT claims_claim_provider_id_45721be3_fk_auth_user_id FOREIGN KEY (provider_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_claimauditlog claims_claimauditlog_actor_id_1101d5f7_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claimauditlog
    ADD CONSTRAINT claims_claimauditlog_actor_id_1101d5f7_fk_auth_user_id FOREIGN KEY (actor_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_claimauditlog claims_claimauditlog_claim_id_1275ed2d_fk_claims_claim_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claimauditlog
    ADD CONSTRAINT claims_claimauditlog_claim_id_1275ed2d_fk_claims_claim_id FOREIGN KEY (claim_id) REFERENCES public.claims_claim(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_claimdocument claims_claimdocument_claim_id_c1c69bf4_fk_claims_claim_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_claimdocument
    ADD CONSTRAINT claims_claimdocument_claim_id_c1c69bf4_fk_claims_claim_id FOREIGN KEY (claim_id) REFERENCES public.claims_claim(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_coverageplan claims_coverageplan_ipm_id_33660a0a_fk_claims_ipm_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_coverageplan
    ADD CONSTRAINT claims_coverageplan_ipm_id_33660a0a_fk_claims_ipm_id FOREIGN KEY (ipm_id) REFERENCES public.claims_ipm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_coveragerule claims_coveragerule_category_id_3ce30a5e_fk_claims_category_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_coveragerule
    ADD CONSTRAINT claims_coveragerule_category_id_3ce30a5e_fk_claims_category_id FOREIGN KEY (category_id) REFERENCES public.claims_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_coveragerule claims_coveragerule_coverage_plan_id_289a27db_fk_claims_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_coveragerule
    ADD CONSTRAINT claims_coveragerule_coverage_plan_id_289a27db_fk_claims_co FOREIGN KEY (coverage_plan_id) REFERENCES public.claims_coverageplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_establishmentpaymentoption claims_establishment_deleted_by_id_d16cf8e7_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_establishmentpaymentoption
    ADD CONSTRAINT claims_establishment_deleted_by_id_d16cf8e7_fk_auth_user FOREIGN KEY (deleted_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_establishmentpaymentoption claims_establishment_hospital_id_ca790a41_fk_claims_ho; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_establishmentpaymentoption
    ADD CONSTRAINT claims_establishment_hospital_id_ca790a41_fk_claims_ho FOREIGN KEY (hospital_id) REFERENCES public.claims_hospital(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_establishmentpaymentoption claims_establishment_payment_method_id_0587b8c6_fk_claims_pa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_establishmentpaymentoption
    ADD CONSTRAINT claims_establishment_payment_method_id_0587b8c6_fk_claims_pa FOREIGN KEY (payment_method_id) REFERENCES public.claims_paymentmethod(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_hospital claims_hospital_deleted_by_id_43fdc6f4_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_hospital
    ADD CONSTRAINT claims_hospital_deleted_by_id_43fdc6f4_fk_auth_user_id FOREIGN KEY (deleted_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_ipm claims_ipm_deleted_by_id_8022a2c0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_ipm
    ADD CONSTRAINT claims_ipm_deleted_by_id_8022a2c0_fk_auth_user_id FOREIGN KEY (deleted_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_ipmpaymentoption claims_ipmpaymentopt_payment_method_id_7fbb0924_fk_claims_pa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_ipmpaymentoption
    ADD CONSTRAINT claims_ipmpaymentopt_payment_method_id_7fbb0924_fk_claims_pa FOREIGN KEY (payment_method_id) REFERENCES public.claims_paymentmethod(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_ipmpaymentoption claims_ipmpaymentoption_deleted_by_id_0ec82b0e_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_ipmpaymentoption
    ADD CONSTRAINT claims_ipmpaymentoption_deleted_by_id_0ec82b0e_fk_auth_user_id FOREIGN KEY (deleted_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_ipmpaymentoption claims_ipmpaymentoption_ipm_id_cb509215_fk_claims_ipm_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_ipmpaymentoption
    ADD CONSTRAINT claims_ipmpaymentoption_ipm_id_cb509215_fk_claims_ipm_id FOREIGN KEY (ipm_id) REFERENCES public.claims_ipm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_notificationlog claims_notificationlog_claim_id_b6e75016_fk_claims_claim_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_notificationlog
    ADD CONSTRAINT claims_notificationlog_claim_id_b6e75016_fk_claims_claim_id FOREIGN KEY (claim_id) REFERENCES public.claims_claim(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_patient claims_patient_coverage_plan_id_6d4b902e_fk_claims_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_patient
    ADD CONSTRAINT claims_patient_coverage_plan_id_6d4b902e_fk_claims_co FOREIGN KEY (coverage_plan_id) REFERENCES public.claims_coverageplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: claims_patient claims_patient_ipm_id_6942c307_fk_claims_ipm_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims_patient
    ADD CONSTRAINT claims_patient_ipm_id_6942c307_fk_claims_ipm_id FOREIGN KEY (ipm_id) REFERENCES public.claims_ipm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict rxSmI8O8r4q8ujTElvx2pqABCL56ATwxV9Gr8bG20OAI1ITTdOSS0C0Bi2QkfCu

