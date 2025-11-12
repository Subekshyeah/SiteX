import React, { useContext } from 'react';
import { MapContext } from '../../contexts/MapContext';
import styles from './Sidebar.module.css';

const Sidebar: React.FC = () => {
    const { mapState, setMapState } = useContext(MapContext);

    const toggle = () => setMapState(s => ({ ...s, sidebarOpen: !s.sidebarOpen }));

    const flyToExample = () => {
        if (mapState.map) mapState.map.flyTo([27.7, 85.3], 13);
    };

    return (
        <aside className={styles.sidebar} style={{ display: mapState.sidebarOpen ? 'block' : 'none' }}>
            <h2 className={styles.title}>Sidebar</h2>
            <ul className={styles.menu}>
                <li className={styles.menuItem}>Item 1</li>
                <li className={styles.menuItem}>Item 2</li>
                <li className={styles.menuItem}>Item 3</li>
                <li className={styles.menuItem}>Item 4</li>
            </ul>
            <button onClick={toggle}>Toggle</button>
            <button onClick={flyToExample}>Go to Kathmandu</button>
        </aside>
    );
};

export default Sidebar;