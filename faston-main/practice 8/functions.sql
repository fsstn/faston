
CREATE OR REPLACE FUNCTION search_phonebook(p_pattern TEXT)
RETURNS TABLE(id INT, name TEXT, surname TEXT, phone TEXT)
LANGUAGE sql
AS $$
    SELECT id, name, surname, phone
    FROM phonebook
    WHERE name ILIKE '%' || p_pattern || '%'
       OR surname ILIKE '%' || p_pattern || '%'
       OR phone ILIKE '%' || p_pattern || '%'
    ORDER BY id;
$$;



CREATE OR REPLACE FUNCTION paginate_phonebook(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name TEXT, surname TEXT, phone TEXT)
LANGUAGE sql
AS $$
    SELECT id, name, surname, phone
    FROM phonebook
    ORDER BY id
    LIMIT p_limit OFFSET p_offset;
$$;