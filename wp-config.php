<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //

define('DB_CHARSET', 'utf8');

define('DB_COLLATE', '');


define('DB_NAME', 'wordpress');
define('DB_USER', 'wordpressuser');
define('DB_PASSWORD', 'wordpress');
define('DB_HOST', 'localhost');
define('AUTH_KEY',         '6nU)u<j,VHIt%{tB^q-pOh+e2d(9*Co=21fESpVPlPa&V0oUl8bGw!u(6WK:]Z0J');
define('SECURE_AUTH_KEY',  'c{XYb]1o$|L+08n1~-D#nAAQHA4LMyAwLbrIlAA./e@L-s9.nov25+oa#wE{D{+G');
define('LOGGED_IN_KEY',    'pFy:^fcV~,wVz1e5lAq-aw_;cp8rKv#UX{+grqB@m|w- ],VxYn(b|J/iq!~=A7l');
define('NONCE_KEY',        'X5 <A($ T5U/|JVXThajFkYe}$$tS+8Aj|&bOyXKUKb(t1[?S@kK)+qX{3wq!0]D');
define('AUTH_SALT',        ')wY1%M6Ev%*O;OLuTkSKDW|<$N&i-TqWy~@lGZV768TXlsOI<a+3<k]U6ww!>r^U');
define('SECURE_AUTH_SALT', '&k$#Ld}j%! as@H?O |-30uZ,eT?YyH2d|trgQ&3a$lG7oz%3PE^Gg-UQS,uLbL?');
define('LOGGED_IN_SALT',   'TV)ai9iphoF,SOP`uwV|JS<h&WHw;+`]^RA)Y+:~uF1D%`9qV*@&Kc]<0:C<Sq4[');
define('NONCE_SALT',       '1V^nwI6le>@40dbA< ]d-X-d1`$e`%0ct}4{:Q/AI-y]8#++)NtGxXO-C.T{A>k>');

define('FS_METHOD', 'direct');
define('FORCE_SSL', true);
define('FORCE_SSL_ADMIN',true);
/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
