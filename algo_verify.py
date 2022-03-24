from tda import auth
import config

try:
        c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome(executable_path='/User/Path') as driver:
                c = auth.client_from_login_flow(driver, config.api_key, config.redirect_url, config.token_path)
