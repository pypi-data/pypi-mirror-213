import React, {useEffect, useState} from 'react';
import {Instance} from "../http/Instance";

const Main = ({setTitle, token}) => {
    const [products, setProducts] = useState([]);

    const getProducts = () => {
        Instance('products', 'GET').then(res => res.json()).then(data => setProducts(data.data))
    }

    useEffect(() => {
        setTitle('Каталог товаров');
        getProducts();
    }, []);
    const addToCart = (e, id) => {
        e.currentTarget.textContent = 'Product in cart'
        e.target.disabled = true
        e.target.style.backgroundColor = '#999'
        Instance(`cart/${id}`, 'POST', token)
    };


    return (
        <main>
            <div className="row row-cols-1 row-cols-md-3 mb-3 text-center">
                {products.map(item =>
                    <div className="col">
                        <div className="card mb-4 rounded-3 shadow-sm">
                            <div className="card-header py-3">
                                <h4 className="my-0 fw-normal">{item.name}</h4>
                            </div>
                            <div className="card-body">
                                <h1 className="card-title pricing-card-title">{item.price}р.</h1>
                                <p>{item.description}</p>
                                {token &&
                                    <button onClick={(e) => addToCart(e, item.id)} type="button"
                                            className="w-100 btn btn-lg btn-outline-success">Добавить в
                                        корзину
                                    </button>}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </main>
    );
};

export default Main;