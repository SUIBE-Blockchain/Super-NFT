import datetime as dt
from super_nft.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)

class Chain(SurrogatePK, Model):
    __tablename__ = "chain"
    name = Column(db.String(88), nullable=False)
    config = Column(db.JSON, default={}, nullable=False)
    height = Column(db.Integer(), nullable=False)
    inserted_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

class Block(SurrogatePK, Model):
    __tablename__ = "blocks"
    chain_id = Column(db.Integer(), nullable=False)
    height = Column(db.Integer(), nullable=False)
    hash = Column(db.String(88), nullable=False)
    inserted_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    timestamp = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    chain_key_id = reference_col("chain", nullable=True)
    chain = relationship("Chain", backref="blocks")

class Transaction(SurrogatePK, Model):
    __tablename__ = "transactions"
    block_id = Column(db.Integer(), nullable=False)
    hash = Column(db.String(88), nullable=False)
    From = Column(db.String(88), nullable=False)
    to = Column(db.String(88), nullable=False)
    inserted_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    contract_id = Column(db.Integer(), nullable=False)
    value = Column(db.DECIMAL(), nullable=False)
    vtho_value = Column(db.DECIMAL(), nullable=False)
    gas = Column(db.DECIMAL(), nullable=False)
    block_key_id = reference_col("blocks", nullable=True)
    block = relationship("Block", backref="transactions")
    contract_key_id = reference_col("contracts", nullable=True)
    contract = relationship("Contract", backref="transactions")

class Contract(SurrogatePK, Model):
    __tablename__ = "contracts"
    addr = Column(db.String(88), nullable=False)
    creater = Column(db.String(88), nullable=False)
    ini_params = Column(db.JSON, default={}, nullable=False)
    description = Column(db.String(88), nullable=False)
    chain_id = Column(db.Integer(), nullable=False)
    contract_template_id = Column(db.Integer(), nullable=False)
    inserted_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    contract_template_key_id = reference_col("contract_template", nullable=True)
    contract_template = relationship("ContractTemplate", backref="contracts")

class ContractTemplate(SurrogatePK, Model):
    __tablename__ = "contract_template"
    name = Column(db.String(88), nullable=False)
    abi = Column(db.JSON, default={}, nullable=False)
    bin = Column(db.String(88), nullable=False)

class Event(SurrogatePK, Model):
    __tablename__ = "events"
    tx_id = Column(db.Integer(), nullable=False)
    log_index = Column(db.Integer(), nullable=False)
    topics = Column(db.JSON, default={}, nullable=False)
    data = Column(db.String(88), nullable=False)
    block_height = Column(db.Integer(), nullable=False)
    contract_id = reference_col("contracts", nullable=True)
    contract = relationship("Contract", backref="events")


