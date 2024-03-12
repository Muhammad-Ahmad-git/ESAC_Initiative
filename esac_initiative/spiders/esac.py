import scrapy


class EsacSpider(scrapy.Spider):
    name = "esac"
    allowed_domains = ["esac-initiative.org"]
    start_urls = ["https://esac-initiative.org/about/transformative-agreements/agreement-registry/"]

    custom_settings = {
        'FEED_FORMAT': 'xlsx',
        'FEED_URI': 'ESAC_Initiative.xlsx',
        'FEED_EXPORTERS': {
            'xlsx': 'scrapy_xlsx.XlsxItemExporter',
        },
    }

    def parse(self, response):
        all_registries = response.xpath("//table[@id='tablepress-10']//tbody//tr")

        for resgistery in all_registries:
            detail_url = resgistery.xpath("./td[7]/a/@href").get('')
            print(f'Detail Url: {detail_url}')

            yield scrapy.Request(detail_url, callback=self.parse_registery_page, dont_filter=True, meta={'detail_url': detail_url})
    
    def parse_registery_page(self, response):
        registery_url = response.meta['detail_url']

        publisher = response.xpath("//td[contains(text(),'Publisher')]/following-sibling::td/h2/text()").get('')
        if not publisher:
            publisher = response.xpath("//td[contains(text(),'Publisher')]/following-sibling::td/text()").get('')
        print(f'Publisher: {publisher}')

        agreement_id = response.xpath("//td[contains(text(),'Agreement ID')]/following-sibling::td/text()").get('')
        if '\n' in agreement_id:
            agreement_id = agreement_id.replcae('\n', '').strip()
        print(f'Agreement Id: {agreement_id}')

        agreement_labeling = response.xpath("//td[contains(text(),'Agreement labeling')]/following-sibling::td/text()").get('')
        print(f'Agreemnet Labeling: {agreement_labeling}')

        agreement_published = response.xpath("//td[contains(text(),'Has the agreement been')]/following-sibling::td/text()").get('')
        print(f'Agreement Published: {agreement_published}')

        url = response.xpath("//td[text()='URL']/following-sibling::td/a/@href").get('')
        print(f'Url: {url}')

        agreement_period = response.xpath("//td[contains(text(),'Agreement period')]/following-sibling::td/text()").get('')
        print(f'Agreement Period: {agreement_period}')

        if agreement_period:
            agreement_period = agreement_period.split("–")
            start_date = agreement_period[0].strip()
            end_date = agreement_period[-1].strip()
        else:
            start_date, end_date = '', ''
        
        print(f'Start Date: {start_date}')
        print(f'End Date: {end_date}')

        consortia_institution = response.xpath("//td[contains(text(),'Consortia / Institution')]/following-sibling::td/text()").get('')
        print(f'Consorita_Institution: {consortia_institution}')

        country = response.xpath("//td[contains(text(),'Country')]/following-sibling::td/text()").get('')
        print(f'Country: {country}')

        size = response.xpath("//strong[contains(text(),'SIZE')]/parent::td/following-sibling::td/text()").get('')
        print(f'Size: {size}')
        
        comments_on_size_output = response.xpath("//strong[text()='Comments on size/article output']/parent::td/following-sibling::td/text()").get('')
        print(f'Comments on size/article output: {comments_on_size_output}')

        cost = response.xpath("//strong[text()='COSTS']/parent::td/following-sibling::td/text()").get('')
        print(f'Cost: {cost}')

        comments_on_cost_development = response.xpath("//strong[text()='Comments on cost development']/parent::td/following-sibling::td/text()").getall()
        if comments_on_cost_development:
            comments_on_cost_development = "".join(comments_on_cost_development)
        else:
            comments_on_cost_development = ''
        print(f'Comments On Cost Development: {comments_on_cost_development}')

        financial_shift = response.xpath("//strong[text()='FINANCIAL SHIFT']/parent::td/following-sibling::td/text()").get('')
        print(f'Financial Shift: {financial_shift}')

        risk_sharing = response.xpath("//strong[text()='RISK SHARING']/parent::td/following-sibling::td/text()").get('')
        print(f'Risk Sharing: {risk_sharing}')

        oa_coverage = response.xpath("//strong[text()='OA COVERAGE']/parent::td/following-sibling::td/text()").get('')
        print(f'OA Coverage: {oa_coverage}')

        fully_open_access_journals_covered = response.xpath("//td[text()='Are fully open access journals covered by the agreement?']/following-sibling::td/text()").get('')
        print(f'Fully Open Access Journals Covered: {fully_open_access_journals_covered}')

        oa_license = response.xpath("//strong[text()='OA LICENSE']/parent::td/following-sibling::td/text()").get('')
        print(f'OA License: {oa_license}')

        article_types = response.xpath("//strong[text()='ARTICLE TYPES']/parent::td/following-sibling::td/text()").getall()
        if article_types:
            article_types = ", ".join(article_types).replace("\n", '').strip()
        print(f'Article Types: {article_types}')

        access_costs = response.xpath("//strong[text()='ACCESS COSTS']/parent::td/following-sibling::td/text()").get('')
        print(f'Access Costs: {access_costs}')

        comments_on_access_costs = response.xpath("//strong[text()='Comments on access costs']/parent::td/following-sibling::td/text()").get('')
        print(f'Comments on access costs: {comments_on_access_costs}')

        access_coverage = response.xpath("//strong[text()='ACCESS COVERAGE']/parent::td/following-sibling::td/text()").get('')
        print(f'Access Coverage: {access_coverage}')

        perpetual_access_rights = response.xpath("//strong[text()='PERPETUAL ACCESS RIGHTS']/parent::td/following-sibling::td/text()").get('')
        print(f'Perpetual Access Rights: {perpetual_access_rights}')

        workflow_assessment = response.xpath("//strong[text()='WORKFLOW ASSESSMENT']/parent::td/following-sibling::td/text()").get('')
        print(f'WorkFlow Accessment: {workflow_assessment}')

        comments_on_workflows = response.xpath("//strong[text()='Comments on workflows']/parent::td/following-sibling::td/text()").get('')
        print(f'Comments On Workflows: {comments_on_workflows}')
    
        overall_assessment_and_comments = response.xpath("//strong[text()='OVERALL ASSESSMENT AND COMMENTS']/parent::td/following-sibling::td/text()").get('')
        print(f'Overall Assessment And Comments: {overall_assessment_and_comments}')
    
        yield {
            'Page Url': registery_url,
            'Publisher': publisher,
            'Agreement ID': agreement_id,
            'Agreement Labeling': agreement_labeling,
            'Agreement Published': agreement_published,
            'URL': url,
            'Start Date': start_date,
            'End Date': end_date,
            'Consortia/Institution': consortia_institution,
            'Country': country,
            'Size': size,
            'Commnets on size/article output': comments_on_size_output,
            'Cost': cost,
            'Comments on Cost Development': comments_on_cost_development,
            'Financial Shift': financial_shift,
            'Risk Sharing': risk_sharing,
            'OA Coverage': oa_coverage,
            'Fully Open Access Journals Covered': fully_open_access_journals_covered,
            'OA License': oa_license,
            'Article Types': article_types,
            'Access Costs': access_costs,
            'Comments on Acess Costs': comments_on_access_costs,
            'Access Coverage': access_coverage,
            'Perpetual Access Rights': perpetual_access_rights,
            'Workflow Assessment': workflow_assessment,
            'Comments on Workflows': comments_on_workflows,
            'Overall Assessment and Comments': overall_assessment_and_comments,
        }