import styles from './styles.module.scss';
import Welcome from 'frames/welcome';
import CompCategorias from 'frames/compCategorias';
import BedCard from 'frames/bedCard';
import NuevProd from 'frames/nuevProd';
import NuevProd0 from '@myImages/nuevProd0.png';
import NuevProd1 from '@myImages/nuevProd1.png';
import NuevProd2 from '@myImages/nuevProd2.png';
import NuevProd3 from '@myImages/nuevProd3.png';
import ComparteSection from 'frames/comparteSection';
import ConocenosImg from '@myImages/conocenos.png';
import Conocenos from 'frames/conocenos';
import Footer from '@myComponents/footer';

export default function Home() {
    return (
        <div className={styles.home}>
            <Welcome />
            <CompCategorias />
            <BedCard />
            <NuevProd imgs={[
                { img: NuevProd0, alt: 'NuevProd0' },
                { img: NuevProd1, alt: 'NuevProd1' },
                { img: NuevProd2, alt: 'NuevProd2' },
                { img: NuevProd3, alt: 'NuevProd3' },
            ]} />
            <ComparteSection />
            <Conocenos img={ConocenosImg} />
            <Footer />
        </div>
    );
}