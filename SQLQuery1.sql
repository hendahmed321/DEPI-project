select * from churn

use churn_DWH;

select * from DimChurn;
select * from DimContract;
select * from DimCustomer;
select * from DimService;
select * from FactCustomerChurn;

drop table FactCustomerChurn;
drop table DimCustomer;
drop table DimContract;
drop table DimChurn;
drop table DimService;




drop table FactCustomerChurn;
drop table DimLocation;

USE [churn_DWH]
GO

/****** Object:  Table [dbo].[FactCustomerChurn]    Script Date: 11/13/2025 11:35:17 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[FactCustomerChurn](
	[FactKey] [int] IDENTITY(1,1) NOT NULL,
	[CustomerKey] [int] NULL,
	[ServiceKey] [int] NULL,
	[ContractKey] [int] NULL,
	[ChurnKey] [int] NULL,
	[TenureMonths] [int] NULL,
	[MonthlyCharges] [decimal](10, 2) NULL,
	[CLTV] [int] NULL,
	[ChurnScore] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[FactKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[FactCustomerChurn]  WITH CHECK ADD FOREIGN KEY([ChurnKey])
REFERENCES [dbo].[DimChurn] ([ChurnKey])
GO

ALTER TABLE [dbo].[FactCustomerChurn]  WITH CHECK ADD FOREIGN KEY([ContractKey])
REFERENCES [dbo].[DimContract] ([ContractKey])
GO

ALTER TABLE [dbo].[FactCustomerChurn]  WITH CHECK ADD FOREIGN KEY([CustomerKey])
REFERENCES [dbo].[DimCustomer] ([CustomerKey])
GO

ALTER TABLE [dbo].[FactCustomerChurn]  WITH CHECK ADD FOREIGN KEY([ServiceKey])
REFERENCES [dbo].[DimService] ([ServiceKey])
GO

USE [churn_DWH]
GO
USE [churn_DWH]
GO

/****** Object:  Table [dbo].[DimCustomer]    Script Date: 11/13/2025 11:38:21 AM ******/
drop table FactCustomerChurn;
drop table DimCustomer;

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimCustomer](
	[CustomerKey] [int] IDENTITY(1,1) NOT NULL,
	[CustomerID] [nvarchar](50) NULL,
	[Gender] [nvarchar](50) NULL,
	[City] [nvarchar](50),
	[SeniorCitizen] [nvarchar](50) NULL,
	[Partner] [nvarchar](50) NULL,
	[Dependents] [nvarchar](50) NULL,
	[ValidFrom] [datetime] NULL,
	[ValidTo] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[CustomerKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[DimCustomer] ADD  DEFAULT (getdate()) FOR [ValidFrom]
GO


alter table Dimservice
drop column HasInternet


drop table DimChurn;
USE [churn_DWH]
GO

/****** Object:  Table [dbo].[DimChurn]    Script Date: 11/13/2025 11:42:38 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimChurn](
	[ChurnKey] [int] IDENTITY(1,1) NOT NULL,
	[ChurnLabel] [nvarchar](50) NULL,
	[ChurnReason] [nvarchar](225) NULL,
	[ValidFrom] [datetime] NULL,
	[ValidTo] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[ChurnKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[DimChurn] ADD  DEFAULT (getdate()) FOR [ValidFrom]
GO

drop table DimContract;
USE [churn_DWH]
GO

/****** Object:  Table [dbo].[DimContract]    Script Date: 11/13/2025 11:43:43 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimContract](
	[ContractKey] [int] IDENTITY(1,1) NOT NULL,
	[ContractType] [nvarchar](50) NULL,
	[PaperlessBilling] [nvarchar](50) NULL,
	[PaymentMethod] [nvarchar](100) NULL,
	[ValidFrom] [datetime] NULL,
	[ValidTo] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[ContractKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[DimContract] ADD  DEFAULT (getdate()) FOR [ValidFrom]
GO

drop table DimService;
USE [churn_DWH]
GO

/****** Object:  Table [dbo].[DimService]    Script Date: 11/13/2025 11:44:49 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimService](
	[ServiceKey] [int] IDENTITY(1,1) NOT NULL,
	[PhoneService] [nvarchar](50) NULL,
	[MultipleLines] [nvarchar](50) NULL,
	[InternetService] [nvarchar](50) NULL,
	[OnlineSecurity] [nvarchar](50) NULL,
	[OnlineBackup] [nvarchar](50) NULL,
	[DeviceProtection] [nvarchar](50) NULL,
	[TechSupport] [nvarchar](50) NULL,
	[StreamingTV] [nvarchar](50) NULL,
	[StreamingMovies] [nvarchar](50) NULL,
	[ValidFrom] [datetime] NULL,
	[ValidTo] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[ServiceKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[DimService] ADD  DEFAULT (getdate()) FOR [ValidFrom]
GO

