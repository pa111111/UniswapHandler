from Repository import PortfolioRepository


def main():
    portfolio = PortfolioRepository.get_portfolio('largeCap')
    print(portfolio.name + ' ' + portfolio.numeraire + ' ' + portfolio.purchase_period)

    for element in portfolio.get_portfolio_elements():
        print(element.asset.name + ' ' + str(element.period_start) + ' ' + str(element.period_end))


main()
