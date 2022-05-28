from paperswithcode import PapersWithCodeClient, models

client = PapersWithCodeClient()
papers = client.paper_list(items_per_page=10)
# for paper in papers.results:
# print(paper)
# print(papers.next_page)

print(papers.count)

print(len(papers.results))
