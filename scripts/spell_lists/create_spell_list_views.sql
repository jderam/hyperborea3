CREATE VIEW v_mag_spell_list AS
SELECT sl.spell_level,
       sl.spell_id,
       s.spell_name,
       sl.d100_min,
       sl.d100_max
  FROM t093_mag_spell_list sl
  JOIN spells s
    ON sl.spell_id = s.spell_id
ORDER BY sl.spell_level, sl.spell_id;

CREATE VIEW v_cry_spell_list AS
SELECT sl.spell_level,
       sl.spell_id,
       s.spell_name,
       sl.d100_min,
       sl.d100_max
  FROM t094_cry_spell_list sl
  JOIN spells s
    ON sl.spell_id = s.spell_id
ORDER BY sl.spell_level, sl.spell_id;

CREATE VIEW v_ill_spell_list AS
SELECT sl.spell_level,
       sl.spell_id,
       s.spell_name,
       sl.d100_min,
       sl.d100_max
  FROM t095_ill_spell_list sl
  JOIN spells s
    ON sl.spell_id = s.spell_id
ORDER BY sl.spell_level, sl.spell_id;

CREATE VIEW v_nec_spell_list AS
SELECT sl.spell_level,
       sl.spell_id,
       s.spell_name,
       sl.d100_min,
       sl.d100_max
  FROM t096_nec_spell_list sl
  JOIN spells s
    ON sl.spell_id = s.spell_id
ORDER BY sl.spell_level, sl.spell_id;

CREATE VIEW v_pyr_spell_list AS
SELECT sl.spell_level,
       sl.spell_id,
       s.spell_name,
       sl.d100_min,
       sl.d100_max
  FROM t097_pyr_spell_list sl
  JOIN spells s
    ON sl.spell_id = s.spell_id
ORDER BY sl.spell_level, sl.spell_id;

CREATE VIEW v_wch_spell_list AS
SELECT sl.spell_level,
       sl.spell_id,
       s.spell_name,
       sl.d100_min,
       sl.d100_max
  FROM t098_wch_spell_list sl
  JOIN spells s
    ON sl.spell_id = s.spell_id
ORDER BY sl.spell_level, sl.spell_id;

CREATE VIEW v_clr_spell_list AS
SELECT sl.spell_level,
       sl.spell_id,
       s.spell_name,
       sl.d100_min,
       sl.d100_max
  FROM t099_clr_spell_list sl
  JOIN spells s
    ON sl.spell_id = s.spell_id
ORDER BY sl.spell_level, sl.spell_id;

CREATE VIEW v_drd_spell_list AS
SELECT sl.spell_level,
       sl.spell_id,
       s.spell_name,
       sl.d100_min,
       sl.d100_max
  FROM t100_drd_spell_list sl
  JOIN spells s
    ON sl.spell_id = s.spell_id
ORDER BY sl.spell_level, sl.spell_id;
