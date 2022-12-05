
CREATE TABLE dbo.[dipendenti](
	[ID] [int] identity(1,1) NOT NULL,
	[NOME] [varchar](255) NULL,
	[COGNOME] [varchar](255) NULL,
	[MAIL] [varchar](255) NULL,
	[DIPARTIMENTO] [varchar](255) NULL,
	[FOTO] [varchar](255) NULL,
 CONSTRAINT [PK_dipendenti] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- DIPARTIMENTO

CREATE TABLE dbo.[dipartimento](
	[ID] [int] identity(1,1) NOT NULL,
	[NOME] [varchar](255) NULL
 CONSTRAINT [PK_dipartamento] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

--EMAIL

CREATE TABLE dbo.[email](
	[ID] [int] identity(1,1) NOT NULL,
	[NOME] [varchar](255) NULL,
	[DESCRIZIONE] [varchar](255) NULL
 CONSTRAINT [PK_email] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- 
CREATE TABLE dbo.[dipendenti_dipartimento](
	[ID_dipen] [int],
	[ID_dipar] [int]
)
GO

CREATE TABLE dbo.[dipendenti_email](
	[ID_dipen] [int],
	[ID_dipar] [int]
)
GO
GO