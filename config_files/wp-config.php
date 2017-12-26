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
define('AUTH_KEY',         'BoO#@b+w3pdH2z$3s(kK,Z>@Lr=OF!sl=}9_)6i>Eekvn;XlHlR|F4Z.}brw&%tR');
define('SECURE_AUTH_KEY',  '=@3;?^nY%Z;5oS y):h2[! Vv({m-UXjZHU8zj2P t}x]FiEylSdr9r)is#L(Pi?');
define('LOGGED_IN_KEY',    'V+rrWgqY9GCOxM_YT~f`Bf*`%dW4ILn0^iuWpPi(`>lnqq)nro]6udFR5(ZYVg1M');
define('NONCE_KEY',        '/Ji^pfG-p~;)7c.qA?|h~D/jr|}srK_I2e_%&h` f+i6<004[K=cEg]Xuv&D*QPZ');
define('AUTH_SALT',        'U`1nXT+1hYDkT+kt9Q.iQ&BPkA4!JRxA=Idn<QYWaDtUUNjx|#(&e|+*.`F6aRg9');
define('SECURE_AUTH_SALT', 't8=t9d;DOZa^J]`+iEEC9A7>|G,=d[+-ySm+dCM$4~6@OvxNfDmH=A-(Y3+,m#^{');
define('LOGGED_IN_SALT',   '>`Dl|~l7ww^-UzS(I>oe::(g~C<:JVQJ Kjlw-Y0U?}`XMD__<fdm&I]9{fjP>ux');
define('NONCE_SALT',       'yt.ZuoVpD{*i+uvQmD(!-4CVf>t~u+7+]vB9`|3T8%kDG7?m_^MAr(yQe8ed_4tD');

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
