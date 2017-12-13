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
define('AUTH_KEY',         'yCW?Q{>zyoYr45UPlmiw Bj.LRJQjlzsCt^-Nm>Rf!k0aHreUFg89Pe5x]apDg|G');
define('SECURE_AUTH_KEY',  'Y`%a{fohvA_~Hg5/ArK-CTJXoa|-#F[|x?UI+1h{_D tD2qv:d.[? ) 2+{8)_K6');
define('LOGGED_IN_KEY',    'XAb`t7@O+|0hhn6x/&zGhZs|xAb{!T_|Cj6(MQ>vna=7Kql2^(|f`aD 0VNc2|uT');
define('NONCE_KEY',        'WV}``_g2Wg0v.ao&$M9+nC@2y`t3kj+If`)Z]:p%E$fYMX%o|vxA%)IP{N [[20Q');
define('AUTH_SALT',        'LP](W|Ug&)%{&mFq{^,X7o|eG0nHzY`:$VuA)lu5H{=f>D7^=XMzrwZZhWaEC+a+');
define('SECURE_AUTH_SALT', 'Sie4uaj%DZt]/J3|x^-S+)A}7}sRjj>(p+$FiBg%i]LHB3.6YF]U!?ZA7%cej(K~');
define('LOGGED_IN_SALT',   'e Cj~d5J|[qYQj[GtT8|7yFN7Tl/4_]I@4tjByI64a/}T;mt}|*]v+$/khibkpdO');
define('NONCE_SALT',       'd5eMi:pxcezm}^P#Ry[y bsicByMyy#1RBx]&N#`Tx>6o,1K)lTh3+Y&kggM3+;6');

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
