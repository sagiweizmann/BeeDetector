<?php
declare(strict_types=1);

namespace App\Infrastructure\Controller\BeeDetector;

use App\Domain\Model\User;
use App\Infrastructure\Controller\DownloadController;
use App\UseCase\User\GetUser;
use Laminas\Diactoros\Response\JsonResponse;
use Symfony\Component\HttpFoundation\File\Exception\FileException;
use Symfony\Component\HttpFoundation\File\UploadedFile;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use TheCodingMachine\GraphQLite\Annotations\Security;

#[Route(path: '/videos')]
final class UploadedVideoController extends DownloadController{

    // upload video
    #[Route(path: '/upload', methods: ['POST'])]
    #[Security("is_granted('IS_AUTHENTICATED_FULLY')")]
    public function uploadVideo(Request $request): JsonResponse
    {
        $uploadedFile = $request->files->get('beeVideo');

        $userId = $request->request->get('userId');

        if (!$uploadedFile instanceof UploadedFile) {
            throw new \InvalidArgumentException('Invalid file uploaded');
        }

        // Generate a unique name for the file before saving it
        $fileName = uniqid().'.'.$uploadedFile->getClientOriginalExtension();
        $target = '';
        $directory = 'bee-videos/' . $userId . '/uploaded-videos/';
        // Move the file to the directory where videos are stored
        try {
            $target = $uploadedFile->move(
                $directory,
                $fileName
            );
        } catch (FileException $e) {
            return new JsonResponse(['error' => $e->getMessage()]);
        }
        $target = $directory . $fileName;
        // You may want to do something else with the file, like saving its path to a database
        // return a json response with the target
        return new JsonResponse(['target' => $target]);
    }
    #[Route(path: '/analyze', methods: ['POST'])]
    #[Security("is_granted('IS_AUTHENTICATED_FULLY')")]
    public function analyzeVideo(Request $request): JsonResponse
    {
        $videoPath = $request->request->get('videoPath');

        $userId = $request->request->get('userId');

        $new_fps = $request->request->get('newFps');

        $min_move_distance = $request->request->get('minMoveDistance');

        $max_move_distance = $request->request->get('maxMoveDistance');

        $realPath = '/var/www/html/public/' . $videoPath;

        $parameters = '--new_fps ' . $new_fps .
                      ' --min_move_distance ' . $min_move_distance .
                      ' --max_move_distance ' . $max_move_distance;

        // Activate the virtual environment first
        try {
            $output = shell_exec('cd /var/www/html/beedetectorai &&
             /var/www/html/beedetectorai/venv/bin/python /var/www/html/beedetectorai/AnalyzeVideo.py '
                . $realPath . ' ' . $parameters);
        } catch (\Exception $e) {
            return new JsonResponse(['error' => $e->getMessage()]);
        }
        //remove the .mp4 from the $videoPath and add _out33.mp4
        $videoOutput  = str_replace('.mp4', '_out33.mp4', $videoPath);
        $csvOutput  = str_replace('.mp4', '_out33.mp4.csv', $videoPath);
        //try chmod the file
        return $this->analyzenconvert($videoOutput, $videoPath, $csvOutput, $realPath, $output, $parameters);
    }
    #[Route(path: '/analyzeflying', methods: ['POST'])]
    #[Security("is_granted('IS_AUTHENTICATED_FULLY')")]
    public function analyzeFlyingVideo(Request $request): JsonResponse
    {
        $videoPath = $request->request->get('videoPath');

        $userId = $request->request->get('userId');

        $realPath = '/var/www/html/public/' . $videoPath;

        $parameters = '';

        // Activate the virtual environment first
        try {
            $output = shell_exec('cd /var/www/html/beedetectorai &&
             /var/www/html/beedetectorai/venv/bin/python /var/www/html/beedetectorai/AnalyzeVideoFlyingBees.py '
                . $realPath . ' ' . $parameters);
        } catch (\Exception $e) {
            return new JsonResponse(['error' => $e->getMessage()]);
        }
        //remove the .mp4 from the $videoPath and add _out33.mp4
        $videoOutput  = str_replace('.mp4', '_out31.mp4', $videoPath);
        $csvOutput  = str_replace('.mp4', '_out31.mp4.csv', $videoPath);
        //try chmod the file
        return $this->analyzenconvert($videoOutput, $videoPath, $csvOutput, $realPath, $output, $parameters);
    }

    /**
     * @param  $videoOutput
     * @param  $videoPath
     * @param  $csvOutput
     * @param string $realPath
     * @param  $output
     * @param string $parameters
     * @return JsonResponse
     */
    protected function analyzenconvert($videoOutput, $videoPath, $csvOutput, string $realPath, $output, string $parameters): JsonResponse {
        try {
            $realPathVideoOutput = '/var/www/html/public/' . $videoOutput;
            $videoOutput = str_replace('.mp4', '_analyzed.mp4', $videoPath);
            $convertedVideoOutput = '/var/www/html/public/' . $videoOutput;
            $realPathCsvOutput = '/var/www/html/public/' . $csvOutput;
            $command = "ffmpeg -i $realPathVideoOutput -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 192k $convertedVideoOutput";
            shell_exec($command);
            unlink($realPathVideoOutput);
            chmod($realPathCsvOutput, 0666);
        } catch (\Exception $e) {
            return new JsonResponse(['error' => $e->getMessage()]);
        }


        return new JsonResponse(['target' => $realPath, 'output' => $output,
            'videoOutput' => $videoOutput, 'csvOutput' => $csvOutput, 'parameters' => $parameters]);
    }
}