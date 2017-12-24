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
define('AUTH_KEY',         'a|Wp`hsl{@O:Z%<SW|l0t|&rmS{,Nex&O`>:CfTh(L;y-k[Bmbp>|s_I#wd]3&|8');
define('SECURE_AUTH_KEY',  ',@/V||jI@Ek$vwvz})=+)P} NjKm~~<H/_TqCKyez|wU#_lvv12x@Hi>Wz0@clZd');
define('LOGGED_IN_KEY',    'yWUd5F3fj:q*cZyW4 BQ7|~d@seUVb:vg+0|UVBciMkCj$@/9{qk)dN_qSO~6+ A');
define('NONCE_KEY',        '8OU,Mjk7qQrV*zF-!.55rw1[%B;O`/^c!3FOP$2t:5:u^;BN@Tohu2tyv([AmvTl');
define('AUTH_SALT',        'hO3aV^`f%PfQb5{v7S$=}qEzSAUo~2]LrvWy?5xb!Pl`7J{Cb=f#l*FY(Or%mjr{');
define('SECURE_AUTH_SALT', ')Z2%a,ZHjg68(z=Vdi(`0(g6:hl+a)*fL.[rm,#X#d)@{.m#?Y3U aq]qi^v= M=');
define('LOGGED_IN_SALT',   'W&9!e9WrTtl*qjJh^Wrfl}Yjc2p2D(7g+Z}y5:gSk6zM)h3VCat.Xp-:,?S m?|2');
define('NONCE_SALT',       '%se6na)-uivD:2N~%Pa,pL+;a!HH_+e2m>:PzWbkfgR;|ESZ3_UAQ=p1uc*g%=N@');

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
