/* =========================================================
   1. Cambio de tipo de datos en la tabla modelo
   ========================================================= */

ALTER TABLE MODELO_UNIDAD
ALTER COLUMN modelo VARCHAR(50) NOT NULL;

/* =========================================================
   1. luego cambiamos los datos por estos:
   ========================================================= */

UPDATE MODELO_UNIDAD SET modelo = 'OF-1721' WHERE id_modelo = 1;
UPDATE MODELO_UNIDAD SET modelo = 'H350'    WHERE id_modelo = 2;
UPDATE MODELO_UNIDAD SET modelo = 'B7R'     WHERE id_modelo = 3;

INSERT INTO MODELO_UNIDAD (id_modelo, modelo) VALUES
(4, 'K310'),
(5, 'Paradiso 1200'),
(6, 'Campione 3.25');