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
define('AUTH_KEY',         'JvU]Aemk{M &pc>2t6T**BEmb9<|W3YY|s2RH<Bf?b6i>&kN-$[OJxfSpd.4m9|q');
define('SECURE_AUTH_KEY',  ' C,j]q@?^Y1*@ yS%T&$Zd >2=iw#pEAAs?,7m5bP+vIY-i+5GU.N,!z;>tEch-_');
define('LOGGED_IN_KEY',    '?#Fd5QC:Jkm@YC-w/89FQ}&tUl*(Vx.B|i|n[d(.%-<FBa}?;ul?;dX!b&Y{~=u1');
define('NONCE_KEY',        'S!2#<|U<~&CUeL`Fd>3%f*^M6,6ia`+?`K3{r!R<>:y3in%;+&L>~8a1mxCn039S');
define('AUTH_SALT',        '*szcVionjdj6XmRK|_e}kSRY/dhj1&hD@EBx$f/j1Q@%i=PoH`)XyK[cx`/iJSHp');
define('SECURE_AUTH_SALT', 'Uz <y#=w@k$j17$}YjQ@+>i:Gd{Zb1qOHCM[e)U!J:{Bs<*&-&:p(@F S^]|p&+c');
define('LOGGED_IN_SALT',   'M|1.Gj1/sHy]Y=5<GK1$=3az>Kq+X8f-GSw:OF+pgEib`kb)=3B|lVY>kF-a2P+[');
define('NONCE_SALT',       'za7z^6(-bh!GrZ4) 3z~<wErVh#l@`vZ`h^,7XsF.R}`Lh-%pu5d|q0NT^Yj|m9(');

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
