create or replace TABLE telemetry (
	timestamp timestamp NOT NULL,
	ts_id varchar not null,
	metric_id varchar not null,
	value float not null
);