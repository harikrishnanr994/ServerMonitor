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
define('AUTH_KEY',         '#gQp(<Us8oik]6Xyn=y}-TJ5QL^9h=%E:]c]UK|{5mbyu1RW)r4~22+#;wS<8ofv');
define('SECURE_AUTH_KEY',  'HdwqiWZ.N!L :5!zSY+dg%3xeg[(!Y*]nsM!PR3}yPtzDP^ w(Pz] Tp<A+2hD[4');
define('LOGGED_IN_KEY',    'xI%L#Mp]A>B4??t:K;,l*xf3C@cPO,Y((+l]pXl[>M44[kRhUtHdaHfIpx,#~m[1');
define('NONCE_KEY',        '-@;!TBF*gg3kUy]nJwis&YEP+go>dHz=OX}vB2Y@F<_%k)S BxPl1$)7u=2R?3;P');
define('AUTH_SALT',        'sFc>>7`&lTcT5k}YHi6qBZA}hiNkJ{3ZKyQ{u~9Y]R-U f3-g+*|5=-$RF3|5BD>');
define('SECURE_AUTH_SALT', 'fomur{Ak+duY-R?vqb)DyL0cx]J+.|=.@lvv;cKyN^jHS7F>vj3ny6`pD#A>wSK+');
define('LOGGED_IN_SALT',   '4_Z(9<xM]xZ=f0 [;DE!rcQC@_#}4(c9HQ<+!K|+MOFHnJY+bUt0)Ayc|bHicg7j');
define('NONCE_SALT',       ':1pH71LV^3nQh 7nhuXB`8z*kzx3`{$+(H8INO4*j;66Umgc2?h$9+P(%:iHvi@Y');

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
