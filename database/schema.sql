CREATE TABLE IF NOT EXISTS `blacklist` (
  `user_id` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `threads` (
  `thread_id` varchar(20) NOT NULL,
  `guild_id` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);