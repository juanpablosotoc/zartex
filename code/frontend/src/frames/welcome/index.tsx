import styles from './styles.module.scss';
import landing from '@myImages/1.png';
import { Link } from 'react-router-dom';
import { ReactComponent as SearchIcon } from '@myIcons/search.svg';
import Button from '@myComponents/button';

export default function Welcome() {
    return (
        <div className={styles.landingContainer}>
            <img src={landing} alt="landing" className={styles.landingImage} loading="lazy" />

            <nav className={styles.nav}>
                <div>
                    <ul>
                        <li>
                            <Link to="/room">
                                Recamara
                            </Link>
                        </li>
                        <li>
                            <Link to="/bathroom">
                                Baño
                            </Link>
                        </li>
                        <li>
                            <Link to="/baby">
                                Bebe
                            </Link>
                        </li>
                        <li>
                            <Link to="/curtains">
                                Cortinas
                            </Link>
                        </li>
                    </ul>
                </div>
                <div className={styles.logoContainer}>
                    <h1>ZARTEX</h1>
                </div>
                <div>
                    <Link to="/search">
                        <button><SearchIcon /></button>
                    </Link>
                </div>
            </nav>
            
            <div className={styles.invitationContainer}>
                <h1>El despertar mas suave de la primavera</h1>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, quos.</p>
                <Link to="/shop">
                    <Button text="Comprar Ahora" />
                </Link>
            </div>
        </div>
    );
};
