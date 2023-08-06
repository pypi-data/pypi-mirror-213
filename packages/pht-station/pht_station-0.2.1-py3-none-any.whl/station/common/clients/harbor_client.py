import os
from typing import List, Union

import requests

from station.app.schemas.local_trains import LocalTrainMasterImageBase
from station.app.schemas.station_status import HealthStatus


class HarborClient:
    def __init__(self, api_url: str = None, username: str = None, password: str = None):
        # Setup and verify connection parameters either based on arguments or .env vars

        self.domain = api_url if api_url else os.getenv("HARBOR_URL")
        self.api_url = self.domain
        if not self.api_url.startswith("https://"):
            self.api_url = "https://" + self.api_url
        if not self.api_url.endswith("/api/v2.0"):
            self.api_url = self.api_url + "/api/v2.0"

        # self.url = self.url.rstrip("/") + "/api/v2.0"

        self.username = username if username else os.getenv("HARBOR_USER")
        assert self.username

        self.password = password if password else os.getenv("HARBOR_PW")
        assert self.password

    def get_artifacts_for_station(
        self, station_id: Union[str, int] = None
    ) -> List[dict]:
        # TODO chache no replys
        if not station_id:
            station_id = int(os.getenv("STATION_ID"))
        assert station_id

        endpoint = f"/projects/station_{station_id}/repositories/"
        r = requests.get(self.api_url + endpoint, auth=(self.username, self.password))
        results = r.json()
        print(results)

        link = True
        while link:
            if r.links:
                if next(iter(r.links)) == "next":
                    print("Getting repositories on next page.")
                    url = r.links["next"]["url"]
                    new_endpoint = url[9:]
                    r = requests.get(
                        self.api_url + new_endpoint, auth=(self.username, self.password)
                    )
                    new_results = r.json()
                    results.extend(new_results)
                else:
                    print("No further repositories found.")
                    link = False
            else:
                # just one page or station not defined
                link = False

        return results

    def get_master_images(self) -> List[LocalTrainMasterImageBase]:
        """
        returns names of master images form harbor
        """
        endpoint = "/projects/master/repositories"
        r = requests.get(self.api_url + endpoint, auth=(self.username, self.password))
        master_images = []
        for repo in r.json():
            project, group, artifact = repo["name"].split("/")
            image_id = f"{self.domain}/{project}/{group}/{artifact}"
            master_images.append(
                LocalTrainMasterImageBase(
                    registry=self.domain,
                    group=group,
                    artifact=artifact,
                    image_id=image_id,
                )
            )

        return master_images

    def health_check(self) -> HealthStatus:
        """
        requests the central service
        @return: dict: status of central harbor instance
        """
        url = self.api_url + "/health"
        try:
            r = requests.get(url=url, auth=(self.username, self.password))
            if r and r.status_code == 200:
                return HealthStatus.healthy
            else:
                return HealthStatus.error
        except requests.exceptions.ConnectionError as e:
            print(e)
        return HealthStatus.error


harbor_client = None
