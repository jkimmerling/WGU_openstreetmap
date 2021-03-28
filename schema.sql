CREATE TABLE nodes (
    id BIGINT PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    node_user TEXT,
    uid_node BIGINT,
    version_node BIGINT,
    changeset BIGINT,
    timestamp_node TEXT
);

CREATE TABLE node_tags (
    id BIGINT,
    node_key TEXT,
    node_value TEXT,
    node_type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id BIGINT PRIMARY KEY NOT NULL,
    way_user TEXT,
    uid_way BIGINT,
    version_way TEXT,
    changeset BIGINT,
    timestamp_way TEXT
);

CREATE TABLE way_tags (
    id BIGINT NOT NULL,
    way_key TEXT NOT NULL,
    way_value TEXT NOT NULL,
    way_type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_node_connections (
    id BIGINT NOT NULL,
    node_id BIGINT NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);