-- MySQL Script generated by MySQL Workbench
-- Sun Nov 26 21:45:15 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema protesto_tcc
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema protesto_tcc
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `protesto_tcc` DEFAULT CHARACTER SET utf8 ;
USE `protesto_tcc` ;

-- -----------------------------------------------------
-- Table `protesto_tcc`.`especies_titulos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protesto_tcc`.`especies_titulos` (
  `cod_especie` CHAR(3) NOT NULL,
  `descricao_especie` TEXT(200) NULL,
  PRIMARY KEY (`cod_especie`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `protesto_tcc`.`codigos_ocorrencia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protesto_tcc`.`codigos_ocorrencia` (
  `cod_ocorrencia` CHAR(1) NOT NULL,
  `descricao_ocorrencia` VARCHAR(45) NULL,
  PRIMARY KEY (`cod_ocorrencia`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `protesto_tcc`.`codigos_irregularidade`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protesto_tcc`.`codigos_irregularidade` (
  `codigo_irregularidade` INT NOT NULL AUTO_INCREMENT,
  `descricao_irregularidade` VARCHAR(90) NULL,
  PRIMARY KEY (`codigo_irregularidade`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `protesto_tcc`.`transacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protesto_tcc`.`transacao` (
  `cod_agencia_cedente` VARCHAR(4) NOT NULL,
  `cod_cedente` VARCHAR(11) NOT NULL,
  `nome_cedente` VARCHAR(45) NOT NULL,
  `nome_sacador` VARCHAR(45) NOT NULL,
  `doc_sacador` VARCHAR(14) NOT NULL,
  `end_sacador` VARCHAR(45) NOT NULL,
  `cep_sacador` VARCHAR(8) NOT NULL,
  `cidade_sacador` VARCHAR(20) NOT NULL,
  `uf_sacador` CHAR(2) NOT NULL,
  `nosso_numero` VARCHAR(15) NOT NULL,
  `especie_titulo` CHAR(3) NOT NULL,
  `num_titulo` VARCHAR(11) NOT NULL,
  `data_emissao` DATE NOT NULL,
  `data_vencimento` DATE NOT NULL,
  `valor_titulo` FLOAT NOT NULL,
  `saldo_titulo` FLOAT NULL,
  `endosso` CHAR(1) NULL,
  `aceite` CHAR(1) NULL,
  `nome_devedor` VARCHAR(45) NOT NULL,
  `tipo_doc_devedor` INT NOT NULL,
  `doc_devedor` VARCHAR(14) NOT NULL,
  `doc_devedor_pf` VARCHAR(11) NULL,
  `endereco_devedor` VARCHAR(45) NOT NULL,
  `cep_devedor` VARCHAR(8) NOT NULL,
  `cidade_devedor` VARCHAR(20) NOT NULL,
  `uf_devedor` CHAR(2) NOT NULL,
  `protocolo` VARCHAR(10) NULL,
  `ocorrencia` CHAR(1) NULL,
  `data_protocolo` DATE NULL,
  `custas_cartorio` FLOAT ZEROFILL NULL,
  `data_ocorrencia` DATE NULL,
  `cod_irregularidade` INT NULL,
  `bairro_devedor` VARCHAR(20) NOT NULL,
  `custas_distribuicao` FLOAT ZEROFILL NULL,
  `compl_cod_irregularidade` VARCHAR(8) NULL,
  `sequencial_remessa` INT NOT NULL,
  PRIMARY KEY (`cod_cedente`, `nosso_numero`),
  UNIQUE INDEX `nosso_numero_UNIQUE` (`nosso_numero` ASC) VISIBLE,
  INDEX `cod_especie_descricao_idx` (`especie_titulo` ASC) VISIBLE,
  INDEX `cod_ocorrencia_descricao_idx` (`ocorrencia` ASC) VISIBLE,
  INDEX `cod_irregularidade_descricao_idx` (`cod_irregularidade` ASC) VISIBLE,
  CONSTRAINT `cod_especie_descricao`
    FOREIGN KEY (`especie_titulo`)
    REFERENCES `protesto_tcc`.`especies_titulos` (`cod_especie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `cod_ocorrencia_descricao`
    FOREIGN KEY (`ocorrencia`)
    REFERENCES `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `cod_irregularidade_descricao`
    FOREIGN KEY (`cod_irregularidade`)
    REFERENCES `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = '		';


-- -----------------------------------------------------
-- Table `protesto_tcc`.`arquivo_remessa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protesto_tcc`.`arquivo_remessa` (
  `sequencial_remessa` INT NOT NULL AUTO_INCREMENT,
  `data_remessa` DATE NULL,
  `confirmacao` TINYINT NULL,
  PRIMARY KEY (`sequencial_remessa`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `protesto_tcc`.`transacao_remessa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protesto_tcc`.`transacao_remessa` (
  `sequencial_remessa` INT NOT NULL,
  `cod_cedente` VARCHAR(45) NOT NULL,
  `nosso_numero` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`sequencial_remessa`, `cod_cedente`, `nosso_numero`),
  INDEX `cod_cedente_remessa_idx` (`cod_cedente` ASC) VISIBLE,
  INDEX `nosso_numero_remessa_idx` (`nosso_numero` ASC) VISIBLE,
  CONSTRAINT `seq_remessa_vinc_transacao`
    FOREIGN KEY (`sequencial_remessa`)
    REFERENCES `protesto_tcc`.`arquivo_remessa` (`sequencial_remessa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `cod_cedente_remessa`
    FOREIGN KEY (`cod_cedente`)
    REFERENCES `protesto_tcc`.`transacao` (`cod_cedente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `nosso_numero_remessa`
    FOREIGN KEY (`nosso_numero`)
    REFERENCES `protesto_tcc`.`transacao` (`nosso_numero`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `protesto_tcc`.`arquivo_retorno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protesto_tcc`.`arquivo_retorno` (
  `data_retorno` DATE NOT NULL,
  `qtd_retorno` INT NULL,
  PRIMARY KEY (`data_retorno`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `protesto_tcc`.`transacao_retorno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protesto_tcc`.`transacao_retorno` (
  `data_retorno` DATE NOT NULL,
  `cod_cedente` VARCHAR(45) NOT NULL,
  `nosso_numero` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`data_retorno`, `cod_cedente`, `nosso_numero`),
  INDEX `cod_cedente_remessa_idx` (`cod_cedente` ASC) VISIBLE,
  INDEX `nosso_numero_remessa_idx` (`nosso_numero` ASC) VISIBLE,
  CONSTRAINT `data_retorno_transacao`
    FOREIGN KEY (`data_retorno`)
    REFERENCES `protesto_tcc`.`arquivo_retorno` (`data_retorno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `cod_cedente_remessa0`
    FOREIGN KEY (`cod_cedente`)
    REFERENCES `protesto_tcc`.`transacao` (`cod_cedente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `nosso_numero_remessa0`
    FOREIGN KEY (`nosso_numero`)
    REFERENCES `protesto_tcc`.`transacao` (`nosso_numero`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `protesto_tcc`;

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `protesto_tcc`.`especies_titulos`
-- -----------------------------------------------------
START TRANSACTION;
USE `protesto_tcc`;
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CBI', 'Cédula de Crédito Bancário por Indicação');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CC', 'Contrato de Câmbio');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CCB', 'Cédula de Crédito Bancário');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CCC', 'Cédula de Crédito Comercial');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CCE', 'Cédula de Crédito à Exportação');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CCI', 'Cédula de Crédito Industrial');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CCR', 'Cédula de Crédito Rural');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CD', 'Confissão de Dívida');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CDA', 'Certidão de Dívida Ativa');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CH', 'Cheque');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CHP', 'Cédula Hipotecária');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CJV', 'Conta Judicialmente Verificada');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CM', 'Contrato de Mútuo');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CPH', 'Cédula Rural Pignoratícia Hipotecária');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CPS', 'Conta de Prestação de Serviços');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CRH', 'Cédula Rural Hipotecária');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CRP', 'Cédula Rural Pignoratícia');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('CT', 'Espécie de Contrato');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('DM', 'Duplicata de Venda Mercantil');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('DMI', 'Duplicata de Venda Mercantil por Indicação');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('DR', 'Duplicata Rural');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('DRI', 'Duplicata Rural por Indicação');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('DS', 'Duplicata de Serviço');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('DSI', 'Duplicata de Serviço por Indicação');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('DV', 'Diversos');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('EC', 'Encargos Condominiais');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('LC', 'Letra de Câmbio');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('NCC', 'Nota de Crédito Comercial');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('NCE', 'Nota de Crédito à Exportação');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('NCI', 'Nota de Crédito Industrial');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('NCR', 'Nota de Crédito Rural');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('NP', 'Nota Promissória');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('NPR', 'Nota Promissória Rural');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('RA', 'Recibo de Aluguel');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('SJ', 'Sentença Judicial');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('TA', 'Termo de Acordo');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('TM', 'Triplicata de Venda Mercantil');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('TS', 'Triplicata de Prestação de Serviços');
INSERT INTO `protesto_tcc`.`especies_titulos` (`cod_especie`, `descricao_especie`) VALUES ('W', 'Warrant');

COMMIT;


-- -----------------------------------------------------
-- Data for table `protesto_tcc`.`codigos_ocorrencia`
-- -----------------------------------------------------
START TRANSACTION;
USE `protesto_tcc`;
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('1', 'Pago');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('2', 'Protestado');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('3', 'Retirado');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('4', 'Sustado');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('5', 'Devolvido Irregular - Sem Custas');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('6', 'Devolvido Irregular - Com Custas');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('7', 'Liquidação Condicional');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('8', 'Título Aceito');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('9', 'Edital');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('A', 'Protesto Cancelado');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('B', 'Protesto Já Efetuado');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('C', 'Protesto por Edital');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('D', 'Retirada por Edital');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('E', 'Protesto de Terceiro Cancelado');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('F', 'Desistência por Liquidação Bancária');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('G', 'Sustado Definitivo');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('I', 'Emissão de 2a Via do IP');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('J', 'Cancelamento Já Efetuado');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('X', 'Cancelamento Não Efetuado');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('0', 'Distribuído');
INSERT INTO `protesto_tcc`.`codigos_ocorrencia` (`cod_ocorrencia`, `descricao_ocorrencia`) VALUES ('Z', 'Aguardando Confirmação');

COMMIT;


-- -----------------------------------------------------
-- Data for table `protesto_tcc`.`codigos_irregularidade`
-- -----------------------------------------------------
START TRANSACTION;
USE `protesto_tcc`;
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (01, 'Data da apresentação inferior à data do vencimento');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (02, 'Falta comprovante da prestação do serviço');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (03, 'Nome do sacado incompleto/incorreto');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (04, 'Nome do cedente incompleto/incorreto');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (05, 'Nome do sacador incompleto/incorreto');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (06, 'Endereço do sacado insuficiente');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (07, 'CNPJ/CPF do sacado inválido/incorreto');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (08, 'CNPJ/CPF incompatível com o nome do sacado');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (09, 'CNPJ/CPF do sacado incompatível com o tipo de documento');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (10, 'CNPJ/CPF do sacador incompatível com a espécie');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (11, 'Título aceito sem a assinatura do sacado');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (12, 'Título aceito rasurado ou rasgado');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (13, 'Título aceito - falta título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (14, 'CEP incorreto');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (15, 'Praça de pagamento incompatível com endereço');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (16, 'Falta número do título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (17, 'Título sem endosso do cedente ou irregular');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (18, 'Falta data de emissão do título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (19, 'Título aceito: valor por extenso diferente do valor numérico');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (20, 'Data da emissão posterior ao vencimento');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (21, 'Espécie inválida para protesto');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (22, 'CEP do sacado incompatível com a praça de protesto');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (23, 'Falta espécie do título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (24, 'Saldo maior que o valor do título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (25, 'Tipo de endosso inválido');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (26, 'Devolvido por ordem judicial');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (27, 'Dados do título não conferem com disquete');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (28, 'Sacado e Sacador são a mesma pessoa');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (29, 'Corrigir a espécie do título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (30, 'Aguardar um dia útil após o vencimento para protestar');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (31, 'Data do vencimento rasurada');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (32, 'Vencimento - extenso não confere com o número');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (33, 'Falta data de vencimento no título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (34, 'DM/DMI sem comprovante autenticado ou declaração');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (35, 'Comprovante ilegível para conferência e microfilmagem');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (36, 'Nome solicitado não confere com emitente ou sacado');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (37, 'Confirmar se são 2 emitentes. Se sim, indicar dados dos 2.');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (38, 'Endereço do sacado igual ao do sacador ou do portador');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (39, 'Endereço do apresentante incompleto ou não informado');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (40, 'Rua / Número inexistente no endereço');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (41, 'Informar a qualidade do endosso (M ou T)');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (42, 'Falta endosso do favorecido para o apresentante');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (43, 'Data da emissão rasurada');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (44, 'Protesto de cheque proibido');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (45, 'Falta assinatura do emitente do cheque');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (46, 'Endereço do emitente no cheque igual ao do banco sacado');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (47, 'Falta o motivo de devolução no cheque ou motivo ilegível');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (48, 'Falta assinatura do sacador no título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (49, 'Nome do apresentante não informado / incompleto / incorreto');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (50, 'Erro de preenchimento do título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (51, 'Título com direito de regresso vencido');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (52, 'Título apresentado em duplicidade');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (53, 'Título já protestado');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (54, 'Letra de câmbio vencida - falta aceite do sacado');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (55, 'Título - falta tradução por tradutor público');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (56, 'Falta declaração de saldo assinada no título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (57, 'Contrato de câmbio - falta conta gráfica');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (58, 'Ausência do documento físico');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (59, 'Sacado falecido');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (60, 'Sacado apresentou quitação do título');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (61, 'Título de outra jurisdição territorial');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (62, 'Título com emissão anterior à concordata do sacado');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (63, 'Sacado não consta na lista de falência');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (64, 'Apresentante não aceita publicação de edital');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (65, 'Dados do sacador em branco ou inválido');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (66, 'Título sem autorização para protesto por edital');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (67, 'Valor divergente entre título e comprovante');
INSERT INTO `protesto_tcc`.`codigos_irregularidade` (`codigo_irregularidade`, `descricao_irregularidade`) VALUES (68, 'Condomínio não pode ser protestado para fins falimentares');

DELIMITER $$
USE `protesto_tcc`$$
CREATE DEFINER = CURRENT_USER TRIGGER `protesto_tcc`.`especies_titulos_BEFORE_INSERT` BEFORE INSERT ON `especies_titulos` FOR EACH ROW
BEGIN
	SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = "Inserção de dados não permitida nesta tabela.";
END;$$

USE `protesto_tcc`$$
CREATE DEFINER = CURRENT_USER TRIGGER `protesto_tcc`.`codigos_ocorrencia_BEFORE_INSERT` BEFORE INSERT ON `codigos_ocorrencia` FOR EACH ROW
BEGIN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'Inserção de Dados Não Permitida para Esta Tabela';
END;$$

USE `protesto_tcc`$$
CREATE DEFINER = CURRENT_USER TRIGGER `protesto_tcc`.`codigos_irregularidade_BEFORE_INSERT` BEFORE INSERT ON `codigos_irregularidade` FOR EACH ROW
BEGIN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'Inserção de dados não permitida para esta tabela.';
END;$$


COMMIT;

