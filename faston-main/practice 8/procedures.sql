CREATE OR REPLACE PROCEDURE insert_or_update_user(
    IN p_name TEXT,
    IN p_surname TEXT,
    IN p_phone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO phonebook(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;



CREATE OR REPLACE PROCEDURE insert_many_users(
    IN p_names TEXT[],
    IN p_surnames TEXT[],
    IN p_phones TEXT[],
    OUT incorrect_data JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 1;
    v_len INT;
BEGIN
    incorrect_data := '[]'::jsonb;
    v_len := COALESCE(array_length(p_names, 1), 0);

    WHILE i <= v_len LOOP
        IF p_phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            INSERT INTO phonebook(name, surname, phone)
            VALUES (p_names[i], p_surnames[i], p_phones[i])
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            incorrect_data := incorrect_data || jsonb_build_array(
                jsonb_build_object(
                    'name', p_names[i],
                    'surname', p_surnames[i],
                    'phone', p_phones[i]
                )
            );
        END IF;

        i := i + 1;
    END LOOP;
END;
$$;



CREATE OR REPLACE PROCEDURE delete_phonebook_data(
    IN p_name TEXT,
    IN p_phone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE (p_name IS NOT NULL AND name = p_name)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;