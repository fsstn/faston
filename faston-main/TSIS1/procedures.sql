-- ============================================================
-- procedures.sql  –  PL/pgSQL objects for TSIS 1
-- ============================================================

-- 1. add_phone
-- find the contact by name and add a new phone number to them
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- figure out the contact id by checking their first or full name
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(first_name || COALESCE(' ' || last_name, '')) = LOWER(TRIM(p_contact_name))
       OR LOWER(first_name) = LOWER(TRIM(p_contact_name))
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    -- make sure they gave a correct phone type
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type "%". Must be home, work, or mobile.', p_type;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);

    RAISE NOTICE 'Phone % (%) added to contact "%".', p_phone, p_type, p_contact_name;
END;
$$;


-- 2. move_to_group
-- move a contact to a group, and make the group if it's missing
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    -- get the contact id first
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(first_name || COALESCE(' ' || last_name, '')) = LOWER(TRIM(p_contact_name))
       OR LOWER(first_name) = LOWER(TRIM(p_contact_name))
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    -- insert group if it's not already in the db
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;

    RAISE NOTICE 'Contact "%" moved to group "%".', p_contact_name, p_group_name;
END;
$$;


-- 3. search_contacts
-- search across everything: name, email, phones
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INTEGER,
    first_name VARCHAR,
    last_name  VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_pattern TEXT := '%' || LOWER(TRIM(p_query)) || '%';
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name
    FROM contacts c
    LEFT JOIN groups g  ON g.id  = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE
        LOWER(c.first_name)                          LIKE v_pattern
        OR LOWER(COALESCE(c.last_name,  ''))         LIKE v_pattern
        OR LOWER(COALESCE(c.email,      ''))         LIKE v_pattern
        OR LOWER(COALESCE(ph.phone,     ''))         LIKE v_pattern
    ORDER BY c.first_name, c.last_name;
END;
$$;
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE (
    id         INTEGER,
    first_name VARCHAR,
    last_name  VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_id   INTEGER,
    created_at TIMESTAMP
) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    ORDER BY first_name, last_name
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;