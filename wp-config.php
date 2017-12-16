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
define('AUTH_KEY',         '-(u[YvmF]U#@!V,{+Y;/KQ<3]b!Rx$j-JbDWrSq39R7K4]D_&l5`#iGX`mztR_g,');
define('SECURE_AUTH_KEY',  'XX1[],AN<fq 9MHgUa^j [.PE^x9oU&RFNfY+<u9a!=erfmS{c(ar{S)( 4lUT-!');
define('LOGGED_IN_KEY',    'nwc:mWM2+WFOz6M6In`_D>IPvGYoGP3T,=|@}Q3;7NduZ>G-;#_Xzob-s#jxQNy7');
define('NONCE_KEY',        '_+n4fUyi85|GKm5j({mID3,n-iJN42p1Q,$|IzF0fU*K|!1I#xNujo3zz<pT:e]-');
define('AUTH_SALT',        'qA]&(.4Ts%#b$TdAj5osgq~jlBw*ROhw2_]h-9|fu<h|*iK9C&v@}$|v~W6A*MC+');
define('SECURE_AUTH_SALT', '9lB]CI35Ir3=e)0M&;{9,sXe%QgJF-A#c+2B-Ssq+>L{[;oC~,b=A+MOc[l=7m^B');
define('LOGGED_IN_SALT',   'I9JFc0#Y-QZ>~N2g34$bgA+)*b<uQ*ZK/lo@p#sK(d+K7~+q3rLaP3uiVGz{sC1c');
define('NONCE_SALT',       'wK$9(T!sTp=kwF|lF[P%5^d~Z2DjY<HX*|pg!{-h8gxR7-S1y}b}8!]:~|*f]x:-');

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
