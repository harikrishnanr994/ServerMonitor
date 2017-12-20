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
define('AUTH_KEY',         'qI4s`@yq32Z0zk]uv-cik:J8(J}8t,jDk+kls&DtrUBRDv?922Nhs,S+)sy[q*ut');
define('SECURE_AUTH_KEY',  ';):vPe+:pW0I*Y9QsRy`(U3B4 cEe-9gxr&B+INo<1;bD:X3t3e/(];d8OnTucD<');
define('LOGGED_IN_KEY',    '1H9o,[DfVB1FBz+jj&|<O-aFroHoA7weHs@a=-B=v9bzA00GyA+WGh(a<qts<|!s');
define('NONCE_KEY',        'nFNwS9ZEk&^2~Tg6QKDLur8MJ16Q)W=kJP)mr|@;2pGLX=Y@GRI[/W9D~-/I,+|a');
define('AUTH_SALT',        'tt*x.d0{SE%-pRR|[ Uc%*9mU Pe2;Q}I+[|-YD0iP#;1@>D-2z(Y~|Nbh+NDjtY');
define('SECURE_AUTH_SALT', 'd&drcB{4i21@j1?4QPpf;7v#bw&~gXWCz:Vf=:<`t|E#7>2h#`Bj0]U7pu?+h@dM');
define('LOGGED_IN_SALT',   'Ze:,J(9y{njXLGbBcqycU~||+p)pvQb.d;~D{uqqGgu~<*iYRE(|VZt2flg~NTyh');
define('NONCE_SALT',       'qvGhm $-@%J~|E76?+&Eybh`(<-HDSmJ;-pmrdeiaF>[flNJ-Y3~_zRBO2`NkS2Q');

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
