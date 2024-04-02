CREATE TABLE ptax (
	sk_data VARCHAR, 
	indicador VARCHAR, 
	valor_dia FLOAT, 
	dt_cadastro TIMESTAMP
)

ALTER TABLE public.ptax ADD CONSTRAINT ptax_unique_constraint UNIQUE (sk_data, indicador);
