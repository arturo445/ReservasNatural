CREATE PROCEDURE [dbo].[GenerarIngresosPorParque]
AS
BEGIN

    SET NOCOUNT ON;

    CREATE TABLE #Ingresos
    (
        Parque VARCHAR(100),
        TotalIngresos DECIMAL(10,2)
    );

    DECLARE @ParqueID INT;
    DECLARE @NombreParque VARCHAR(100);
    DECLARE @Total DECIMAL(10,2);

   DECLARE cursor_ingresos CURSOR FOR
SELECT P.Parque_ID,
       P.Nombre,
       SUM(E.Precio)
FROM Entradas E
INNER JOIN Parques P
    ON E.Parque_ID = P.Parque_ID
GROUP BY P.Parque_ID, P.Nombre
ORDER BY SUM(E.Precio) ASC;

    OPEN cursor_ingresos;

    FETCH NEXT FROM cursor_ingresos
    INTO @ParqueID, @NombreParque, @Total;

    WHILE @@FETCH_STATUS = 0
    BEGIN

        INSERT INTO #Ingresos
        VALUES (@NombreParque, @Total);

        FETCH NEXT FROM cursor_ingresos
        INTO @ParqueID, @NombreParque, @Total;
    END;

    CLOSE cursor_ingresos;
    DEALLOCATE cursor_ingresos;

    SELECT *
    FROM #Ingresos;

END;